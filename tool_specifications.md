# BI Migration Agent - Detailed Tool Specifications

## Tool 1: MicroStrategy Object Analyzer

### Purpose
Parses and analyzes MicroStrategy objects to understand structure, complexity, dependencies, and migration effort estimation.

### Configuration
```yaml
Tool ID: tool_mstr_analyzer
Category: Analysis
Complexity Level: High
Requires Authentication: Yes (MicroStrategy API)
Async Support: Yes (for large environments)
Timeout: 120 seconds
```

### Input Schema
```json
{
  "object_name": {
    "type": "string",
    "description": "Name of MicroStrategy object",
    "required": true,
    "example": "Executive Sales Dashboard"
  },
  "object_type": {
    "type": "string",
    "enum": ["report", "metric", "hierarchy", "filter", "attribute", "fact", "prompt"],
    "description": "Classification of object",
    "required": true
  },
  "definition_format": {
    "type": "string",
    "enum": ["xml", "json", "mstr_api"],
    "description": "Format of object definition",
    "required": true
  },
  "definition_content": {
    "type": "string",
    "description": "Object definition (XML, JSON, or API response)",
    "required": true,
    "max_length": 1000000
  },
  "environment_context": {
    "type": "object",
    "description": "Metadata about the MicroStrategy environment",
    "properties": {
      "version": {"type": "string", "example": "2023.10"},
      "data_warehouse": {"type": "string", "example": "SQL Server 2019"},
      "fact_table_row_count": {"type": "integer"}
    }
  }
}
```

### Output Schema
```json
{
  "analysis_id": "string (UUID of analysis)",
  "object_name": "string",
  "object_type": "string",
  "structure_analysis": {
    "element_count": "integer",
    "levels": "integer",
    "has_custom_logic": "boolean",
    "calculation_complexity": "string (Low|Medium|High|Very High)"
  },
  "dependencies": {
    "referenced_objects": [
      {
        "name": "string",
        "type": "string",
        "impact": "string (Direct|Indirect|Optional)"
      }
    ],
    "data_sources": ["string array"],
    "total_dependencies": "integer"
  },
  "complexity_metrics": {
    "cyclomatic_complexity": "integer (0-100)",
    "nesting_depth": "integer",
    "function_count": "integer",
    "formula_length": "integer"
  },
  "migration_assessment": {
    "complexity_score": "integer (0-100)",
    "migration_effort": "string (Low|Medium|High|Very High|Extreme)",
    "estimated_hours": "number",
    "risk_level": "string (Low|Medium|High|Critical)",
    "risk_factors": ["string array"],
    "recommended_approach": "string"
  },
  "power_bi_equivalent": {
    "suggested_pattern": "string",
    "alternative_patterns": ["string array"],
    "implementation_notes": "string"
  },
  "validation_checkpoints": [
    "string array - specific tests to run after migration"
  ]
}
```

### Usage Examples

**Example 1: Analyze Complex Metric**
```
Input: Analyze metric "Revenue YoY Growth %" (nested calculate, time logic)
Output:
  - Complexity Score: 72/100 → High
  - Migration Effort: 8-10 hours
  - Risk Factors: ["Fiscal calendar handling", "Leap year edge case"]
  - Recommended Approach: "Use DAX with CALCULATE + DATEADD, test for calendar edge cases"
```

**Example 2: Analyze Ragged Hierarchy**
```
Input: Analyze hierarchy "Geography" with missing levels
Output:
  - Complexity Score: 58/100 → Medium-High
  - Migration Effort: 6-8 hours
  - Risk Factors: ["Ragged structure complicates Power BI hierarchy"]
  - Recommended Approach: "Denormalize to levels, create bridge table for ragged branches"
```

---

## Tool 2: DAX Formula Generator

### Purpose
Converts MicroStrategy metric definitions into Power BI DAX measures with validation and optimization.

### Configuration
```yaml
Tool ID: tool_dax_generator
Category: Code Generation
Complexity Level: Very High
Requires Authentication: No
Async Support: Yes
Timeout: 60 seconds
Max Formula Length: 50000 characters
```

### Input Schema
```json
{
  "metric_definition": {
    "type": "string",
    "description": "MicroStrategy metric logic (human-readable or formula)",
    "required": true,
    "example": "Sum of Revenue where Fiscal Year = Current Year"
  },
  "context": {
    "type": "object",
    "description": "Dimensional and fact table context",
    "properties": {
      "fact_table_name": {"type": "string"},
      "measure_column": {"type": "string"},
      "dimension_tables": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "table_name": "string",
            "columns": ["string array"],
            "type": "string (standard|role-playing|slowly_changing)"
          }
        }
      },
      "custom_hierarchies": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "hierarchy_name": "string",
            "levels": ["string array"]
          }
        }
      }
    },
    "required": true
  },
  "parameters": {
    "type": "object",
    "properties": {
      "data_type": {"type": "string", "enum": ["currency", "percentage", "number", "text"]},
      "number_format": {"type": "string", "example": "$#,##0.00"},
      "requires_time_intelligence": {"type": "boolean"},
      "performance_tier": {"type": "string", "enum": ["fast", "balanced", "complex"]},
      "target_power_bi_version": {"type": "string", "default": "2024.1"}
    }
  }
}
```

### Output Schema
```json
{
  "formula_id": "string (UUID)",
  "metric_name": "string",
  "dax_formula": {
    "primary": "string (the main DAX measure)",
    "supporting_measures": ["string array (if intermediate measures needed)"],
    "calculated_columns": ["string array (if helper columns needed)"]
  },
  "formula_analysis": {
    "is_valid_syntax": "boolean",
    "syntax_errors": ["string array"],
    "compilation_notes": "string"
  },
  "performance_assessment": {
    "estimated_execution_time_ms": "integer",
    "query_folding_compatible": "boolean",
    "query_folding_notes": "string",
    "optimization_recommendations": [
      {
        "recommendation": "string",
        "impact": "string (High|Medium|Low)",
        "effort": "string (Low|Medium|High)"
      }
    ]
  },
  "validation_metadata": {
    "expected_result_type": "string (decimal, integer, text)",
    "sample_test_case": {
      "input_context": "object",
      "expected_output": "number or string"
    },
    "validation_formula": "string (formula to verify result)"
  },
  "alternative_implementations": [
    {
      "approach": "string",
      "pros": ["string array"],
      "cons": ["string array"],
      "complexity_score": "integer"
    }
  ],
  "documentation": {
    "business_logic_summary": "string",
    "assumptions": ["string array"],
    "limitations": ["string array"],
    "edge_cases": ["string array"],
    "code_comments": "string"
  }
}
```

### Usage Examples

**Example 1: Simple Aggregation**
```
Input: "Total Sales Revenue (Sum of Amount)"
Output DAX:
  Total Sales Revenue = SUM('Fact Sales'[Amount])
  
Performance: <10ms
Optimization: None needed
```

**Example 2: Complex Calculation with Time Logic**
```
Input: "YTD Sales with comparison to previous year same month"
Output DAX:
  YTD Sales = TOTALMTD(SUM('Fact Sales'[Amount]), 'Date'[DateKey])
  Prior Month YTD = CALCULATE([YTD Sales], DATEADD('Date'[DateKey], -1, MONTH))
  YTD vs Prior Month % = DIVIDE([YTD Sales] - [Prior Month YTD], [Prior Month YTD], 0)

Supporting Measures: 3
Performance: 50-100ms depending on data volume
Optimization: Consider aggregation table if >50M rows
```

---

## Tool 3: Transformation Validator

### Purpose
Compares results from MicroStrategy and Power BI to identify discrepancies and validate migration accuracy.

### Configuration
```yaml
Tool ID: tool_transform_validator
Category: Quality Assurance
Complexity Level: High
Requires Authentication: Yes (both systems)
Async Support: Yes
Timeout: 300 seconds (large result sets)
Max Result Set Size: 1000000 rows
```

### Input Schema
```json
{
  "validation_type": {
    "type": "string",
    "enum": ["measure_comparison", "row_level_match", "aggregate_match", "filter_validation"],
    "required": true
  },
  "mstr_query_result": {
    "type": "object",
    "description": "Original MicroStrategy query output",
    "required": true,
    "properties": {
      "columns": ["string array"],
      "rows": [{"type": "array"}],
      "metadata": {"type": "object"}
    }
  },
  "powerbi_query_result": {
    "type": "object",
    "description": "Power BI query output (DAX query)",
    "required": true,
    "properties": {
      "columns": ["string array"],
      "rows": [{"type": "array"}],
      "metadata": {"type": "object"}
    }
  },
  "validation_rules": {
    "type": "object",
    "properties": {
      "numeric_tolerance": {
        "type": {"type": "string", "enum": ["absolute", "percentage"]},
        "value": "number",
        "example": {"type": "percentage", "value": 0.5}
      },
      "ignore_columns": ["string array"],
      "key_columns": {
        "type": "array of columns that define row uniqueness",
        "example": ["Year", "Month", "Region", "Product"]
      }
    }
  }
}
```

### Output Schema
```json
{
  "validation_id": "string (UUID)",
  "validation_timestamp": "date-time",
  "overall_status": "string (PASS|FAIL|PARTIAL)",
  "match_summary": {
    "total_rows_mstr": "integer",
    "total_rows_powerbi": "integer",
    "rows_matched": "integer",
    "rows_unmatched": "integer",
    "match_percentage": "number (0-100)"
  },
  "column_analysis": [
    {
      "column_name": "string",
      "data_type_match": "boolean",
      "sample_values_match": "boolean",
      "aggregate_match": "boolean",
      "max_variance": "number",
      "status": "string (MATCH|MISMATCH|UNDER_TOLERANCE)"
    }
  ],
  "discrepancy_details": [
    {
      "row_key": "object (key columns)",
      "mstr_value": "number or string",
      "powerbi_value": "number or string",
      "variance": "number",
      "variance_type": "string (Absolute|Percentage)",
      "within_tolerance": "boolean",
      "likely_cause": "string"
    }
  ],
  "root_cause_analysis": [
    {
      "issue_type": "string (Precision loss|Null handling|Filter logic|etc)",
      "affected_rows": "integer",
      "recommendation": "string",
      "severity": "string (High|Medium|Low)"
    }
  ],
  "validation_actions": {
    "action_required": "boolean",
    "recommended_actions": ["string array"],
    "approval_needed": "boolean"
  }
}
```

---

## Tool 4: Security Model Mapper

### Purpose
Translates MicroStrategy security filters and element-level security to Power BI RLS rules.

### Configuration
```yaml
Tool ID: tool_security_mapper
Category: Security & Compliance
Complexity Level: Very High
Requires Authentication: Yes (MicroStrategy + AD)
Async Support: No (security-sensitive)
Timeout: 30 seconds
Sensitive Data: Yes (logs not stored)
```

### Input Schema
```json
{
  "security_type": {
    "type": "string",
    "enum": ["element_security", "security_filter", "role_based", "hierarchy_based"],
    "required": true
  },
  "security_definition": {
    "type": "string",
    "description": "MicroStrategy security rule",
    "required": true,
    "example": "User sees only [Region] = CurrentUserRegion"
  },
  "user_structure": {
    "type": "object",
    "properties": {
      "user_source": "string (ActiveDirectory|LDAP|Custom)",
      "user_attributes": ["string array: email, department, region, etc"],
      "user_groups": ["string array"],
      "hierarchy_levels": ["string array: if hierarchical security"]
    },
    "required": true
  },
  "target_model_context": {
    "type": "object",
    "properties": {
      "dimension_tables": ["string array"],
      "secure_columns": ["string array"],
      "user_mapping_table": "string"
    },
    "required": true
  }
}
```

### Output Schema
```json
{
  "mapping_id": "string (UUID)",
  "security_type": "string",
  "rls_configurations": [
    {
      "rule_name": "string",
      "powerbi_role_name": "string",
      "rls_dax_formula": "string",
      "applicable_to_tables": ["string array"],
      "complexity_score": "integer (0-100)"
    }
  ],
  "user_mapping": {
    "mapping_strategy": "string (Static Table|Dynamic LDAP|Mixed)",
    "user_mapping_table_required": "boolean",
    "mapping_table_design": {
      "table_name": "string",
      "columns": [{"column_name": "string", "source": "string"}]
    }
  },
  "implementation_steps": [
    "string (step-by-step implementation)"
  ],
  "testing_plan": {
    "test_users": [
      {
        "user_id": "string",
        "expected_visible_records": "integer",
        "test_queries": ["string array"]
      }
    ],
    "validation_checklist": ["string array"]
  },
  "migration_notes": {
    "equivalent_accuracy": "string (Exact|Close|Different Approach)",
    "limitations": ["string array"],
    "recommendations": ["string array"]
  }
}
```

---

## Tool 5: Migration Report Generator

### Purpose
Creates comprehensive migration documentation and progress reports for stakeholders.

### Configuration
```yaml
Tool ID: tool_report_generator
Category: Reporting & Documentation
Complexity Level: Medium
Requires Authentication: No
Async Support: Yes
Timeout: 60 seconds
Output Formats: ["Markdown", "PDF", "Excel", "HTML"]
```

### Input Schema
```json
{
  "report_type": {
    "type": "string",
    "enum": ["status", "technical", "executive_summary", "transformation_mapping", "test_results", "knowledge_transfer"],
    "required": true
  },
  "migration_data": {
    "type": "object",
    "properties": {
      "project_name": "string",
      "status": "string (Planning|In Progress|Testing|Cutover|Complete)",
      "phase": "integer (1-6)",
      "overall_completion_percentage": "integer (0-100)",
      "timeline": {
        "planned_start": "date",
        "planned_end": "date",
        "actual_start": "date",
        "actual_current": "date"
      },
      "artifacts": [
        {
          "name": "string",
          "type": "string",
          "status": "string",
          "metrics": {}
        }
      ],
      "issues_log": [
        {
          "id": "string",
          "title": "string",
          "severity": "string",
          "status": "string",
          "resolution": "string"
        }
      ],
      "lessons_learned": ["string array"]
    },
    "required": true
  },
  "output_format": {
    "type": "string",
    "enum": ["markdown", "pdf", "html", "excel"],
    "default": "markdown"
  }
}
```

### Output Schema
```json
{
  "report_id": "string (UUID)",
  "report_type": "string",
  "generated_timestamp": "date-time",
  "document": {
    "content": "string (Markdown, HTML, or PDF binary)",
    "file_format": "string",
    "file_size_bytes": "integer"
  },
  "metadata": {
    "page_count": "integer (if PDF)",
    "section_count": "integer",
    "tables": "integer",
    "charts": "integer"
  },
  "executive_summary": {
    "status": "string (Green|Yellow|Red)",
    "key_metrics": "object",
    "risks": ["string array"],
    "next_steps": ["string array"]
  }
}
```

---

## Tool 6: Model Performance Analyzer

### Purpose
Analyzes Power BI semantic model performance and provides optimization recommendations.

### Configuration
```yaml
Tool ID: tool_performance_analyzer
Category: Performance & Optimization
Complexity Level: High
Requires Authentication: Yes (Power BI)
Async Support: Yes
Timeout: 120 seconds
```

### Input Schema
```json
{
  "model_definition": {
    "type": "object",
    "description": "Power BI semantic model metadata",
    "properties": {
      "tables": [
        {
          "name": "string",
          "row_count": "integer",
          "column_count": "integer",
          "relationship_count": "integer"
        }
      ],
      "measures": [
        {
          "name": "string",
          "formula": "string",
          "data_type": "string"
        }
      ]
    }
  },
  "workload_characteristics": {
    "type": "object",
    "properties": {
      "expected_concurrent_users": "integer",
      "typical_report_complexity": "string (Simple|Medium|Complex)",
      "data_volume_gb": "number",
      "refresh_frequency": "string (hourly|daily|weekly)"
    }
  }
}
```

### Output Schema
```json
{
  "analysis_id": "string",
  "overall_performance_score": "integer (0-100)",
  "performance_rating": "string (Excellent|Good|Fair|Poor|Critical)",
  "bottleneck_analysis": [
    {
      "bottleneck": "string",
      "impact": "string (High|Medium|Low)",
      "affected_component": "string"
    }
  ],
  "recommendations": [
    {
      "recommendation": "string",
      "priority": "string (Critical|High|Medium|Low)",
      "estimated_improvement_percent": "integer",
      "implementation_effort": "string"
    }
  ],
  "performance_benchmarks": {
    "estimated_query_time_ms": "integer",
    "estimated_refresh_time_minutes": "integer",
    "model_size_mb": "integer"
  }
}
```

---

## Tool Orchestration Order

### For Complete Migration:
1. **Start:** MicroStrategy Object Analyzer (understand source)
2. **Design:** Security Model Mapper (define security)
3. **Design:** Area: DAX Formula Generator (create measures)
4. **Build:** Implement in Power BI
5. **Validate:** Transformation Validator (compare results)
6. **Optimize:** Model Performance Analyzer (tune)
7. **Report:** Migration Report Generator (document)

### Error Handling:
- If Transformation Validator finds variance > tolerance:
  1. Review DAX Formula Generator recommendations
  2. Modify DAX formula
  3. Re-run Transformation Validator
  4. Document root cause

