#ifndef DUCKDB_SOURCE_ID
#define DUCKDB_SOURCE_ID "d9bceddc7209a7e0b5c0402958d1191e19a491e7"
#endif
#include "duckdb/function/table/sqlite_functions.hpp"
#include "duckdb/main/database.hpp"

namespace duckdb {

struct PragmaVersionData : public TableFunctionData {
	PragmaVersionData() : done(false) {
	}
	bool done;
};

static unique_ptr<FunctionData> pragma_version_bind(ClientContext &context, vector<Value> &inputs,
                                                    unordered_map<string, Value> &named_parameters,
                                                    vector<LogicalType> &return_types, vector<string> &names) {
	names.push_back("library_version");
	return_types.push_back(LogicalType::VARCHAR);
	names.push_back("source_id");
	return_types.push_back(LogicalType::VARCHAR);

	return make_unique<PragmaVersionData>();
}

static void pragma_version_info(ClientContext &context, vector<Value> &input, DataChunk &output,
                                FunctionData *dataptr) {
	auto &data = *((PragmaVersionData *)dataptr);
	assert(input.size() == 0);
	if (data.done) {
		// finished returning values
		return;
	}
	output.SetCardinality(1);
	output.SetValue(0, 0, DuckDB::LibraryVersion());
	output.SetValue(1, 0, DuckDB::SourceID());
	data.done = true;
}

void PragmaVersion::RegisterFunction(BuiltinFunctions &set) {
	set.AddFunction(TableFunction("pragma_version", {}, pragma_version_bind, pragma_version_info, nullptr));
}

const char *DuckDB::SourceID() {
	return DUCKDB_SOURCE_ID;
}

const char *DuckDB::LibraryVersion() {
	return "DuckDB";
}

} // namespace duckdb
