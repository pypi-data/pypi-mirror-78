//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/execution/operator/helper/physical_pragma.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/execution/physical_operator.hpp"
#include "duckdb/parser/parsed_data/pragma_info.hpp"

namespace duckdb {

//! PhysicalPragma represents the PRAGMA operator
class PhysicalPragma : public PhysicalOperator {
public:
	PhysicalPragma(unique_ptr<PragmaInfo> info)
	    : PhysicalOperator(PhysicalOperatorType::PRAGMA, {LogicalType::BOOLEAN}), info(move(info)) {
	}

	unique_ptr<PragmaInfo> info;

public:
	void GetChunkInternal(ExecutionContext &context, DataChunk &chunk, PhysicalOperatorState *state) override;
};

} // namespace duckdb
