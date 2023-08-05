#include "duckdb/parallel/pipeline.hpp"

#include "duckdb/common/printer.hpp"
#include "duckdb/execution/executor.hpp"
#include "duckdb/main/client_context.hpp"
#include "duckdb/parallel/task_context.hpp"
#include "duckdb/parallel/thread_context.hpp"
#include "duckdb/parallel/task_scheduler.hpp"

#include "duckdb/execution/operator/aggregate/physical_simple_aggregate.hpp"
#include "duckdb/execution/operator/scan/physical_table_scan.hpp"
#include "duckdb/execution/operator/aggregate/physical_hash_aggregate.hpp"

using namespace std;

namespace duckdb {

class PipelineTask : public Task {
public:
	PipelineTask(Pipeline *pipeline_) : pipeline(pipeline_) {
	}

	TaskContext task;
	Pipeline *pipeline;

public:
	void Execute() override {
		pipeline->Execute(task);
		pipeline->FinishTask();
	}
};

Pipeline::Pipeline(Executor &executor_)
    : executor(executor_), finished_dependencies(0), finished(false), finished_tasks(0), total_tasks(0) {
}

void Pipeline::Execute(TaskContext &task) {
	assert(finished_dependencies == dependencies.size());

	auto &client = executor.context;
	if (client.interrupted) {
		return;
	}

	ThreadContext thread(client);
	ExecutionContext context(client, thread, task);
	try {
		auto state = child->GetOperatorState();
		auto lstate = sink->GetLocalSinkState(context);
		// incrementally process the pipeline
		DataChunk intermediate;
		child->InitializeChunk(intermediate);
		while (true) {
			child->GetChunk(context, intermediate, state.get());
			thread.profiler.StartOperator(sink);
			if (intermediate.size() == 0) {
				sink->Combine(context, *sink_state, *lstate);
				break;
			}
			sink->Sink(context, *sink_state, *lstate, intermediate);
			thread.profiler.EndOperator(nullptr);
		}
	} catch (std::exception &ex) {
		executor.PushError(ex.what());
	} catch (...) {
		executor.PushError("Unknown exception in pipeline!");
	}
	executor.Flush(thread);
}

void Pipeline::FinishTask() {
	assert(finished_tasks < total_tasks);
	idx_t current_finished = ++finished_tasks;
	if (current_finished == total_tasks) {
		try {
			sink->Finalize(executor.context, move(sink_state));
		} catch(std::exception &ex) {
			executor.PushError(ex.what());
		} catch (...) {
			executor.PushError("Unknown exception in Finalize!");
		}
		Finish();
	}
}

void Pipeline::ScheduleSequentialTask() {
	auto &scheduler = TaskScheduler::GetScheduler(executor.context);
	auto task = make_unique<PipelineTask>(this);

	this->total_tasks = 1;
	scheduler.ScheduleTask(*executor.producer, move(task));
}

bool Pipeline::ScheduleOperator(PhysicalOperator *op) {
	switch (op->type) {
	case PhysicalOperatorType::FILTER:
	case PhysicalOperatorType::PROJECTION:
	case PhysicalOperatorType::HASH_JOIN:
		// filter, projection or hash probe: continue in children
		return ScheduleOperator(op->children[0].get());
	case PhysicalOperatorType::SEQ_SCAN: {
		// we reached a scan: split it up into parts and schedule the parts
		auto &scheduler = TaskScheduler::GetScheduler(executor.context);

		// first we gather all of the tasks of this pipeline
		// we gather the tasks first because we want to set total_tasks to the actual task amount
		// otherwise we can encounter race conditions in which a pipeline could finish twice
		vector<unique_ptr<OperatorTaskInfo>> tasks;
		op->ParallelScanInfo(executor.context, [&](unique_ptr<OperatorTaskInfo> info) { tasks.push_back(move(info)); });
		this->total_tasks = tasks.size();
		if (this->total_tasks == 0) {
			// could not generate parallel tasks, or parallel tasks were determined as not worthwhile
			// move on to sequential execution
			return false;
		}
		// after we have gathered all the tasks we actually schedule them for execution
		for (auto &info : tasks) {
			auto task = make_unique<PipelineTask>(this);
			task->task.task_info[op] = move(info);
			scheduler.ScheduleTask(*executor.producer, move(task));
		}
		return true;
	}
	case PhysicalOperatorType::HASH_GROUP_BY: {
		// FIXME: parallelize scan of GROUP_BY HT
		return false;
	}
	default:
		// unknown operator: skip parallel task scheduling
		return false;
	}
}

void Pipeline::Schedule() {
	assert(finished_tasks == 0);
	assert(total_tasks == 0);
	assert(finished_dependencies == dependencies.size());
	// check if we can parallelize this task based on the sink
	switch (sink->type) {
	case PhysicalOperatorType::SIMPLE_AGGREGATE: {
		auto &simple_aggregate = (PhysicalSimpleAggregate &)*sink;
		// simple aggregate: check if we can parallelize it
		if (!simple_aggregate.all_combinable) {
			// not all aggregates are parallelizable: switch to sequential mode
			break;
		}
		if (ScheduleOperator(sink->children[0].get())) {
			// all parallel tasks have been scheduled: return
			return;
		}
		break;
	}
	case PhysicalOperatorType::HASH_GROUP_BY: {
		auto &hash_aggr = (PhysicalHashAggregate &)*sink;
		if (!hash_aggr.all_combinable) {
			// not all aggregates are parallelizable: switch to sequential mode
			break;
		}
		if (ScheduleOperator(sink->children[0].get())) {
			// all parallel tasks have been scheduled: return
			return;
		}
		break;
	}
	case PhysicalOperatorType::HASH_JOIN: {
		// schedule build side of the join
		if (ScheduleOperator(sink->children[1].get())) {
			// all parallel tasks have been scheduled: return
			return;
		}
		break;
	}
	default:
		break;
	}
	// could not parallelize this pipeline: push a sequential task instead
	ScheduleSequentialTask();
}

void Pipeline::AddDependency(Pipeline *pipeline) {
	this->dependencies.insert(pipeline);
	pipeline->parents.insert(this);
}

void Pipeline::CompleteDependency() {
	idx_t current_finished = ++finished_dependencies;
	if (current_finished == dependencies.size()) {
		// all dependencies have been completed: schedule the pipeline
		Schedule();
	}
}

void Pipeline::Finish() {
	assert(!finished);
	finished = true;
	// finished processing the pipeline, now we can schedule pipelines that depend on this pipeline
	for (auto &parent : parents) {
		// mark a dependency as completed for each of the parents
		parent->CompleteDependency();
	}
	executor.completed_pipelines++;
}

string Pipeline::ToString() const {
	string str = PhysicalOperatorToString(sink->type);
	auto node = this->child;
	while (node) {
		str = PhysicalOperatorToString(node->type) + " -> " + str;
		node = node->children[0].get();
	}
	return str;
}

void Pipeline::Print() const {
	Printer::Print(ToString());
}

} // namespace duckdb
