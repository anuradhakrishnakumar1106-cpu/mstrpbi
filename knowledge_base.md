# MicroStrategy to Power BI Migration Knowledge Base

## 1. MicroStrategy Architecture Reference

### Report Types
| Type | Description | Power BI Equivalent | Complexity |
|------|-------------|-------------------|-----------|
| Standard Report | Basic query with attributes and metrics | Table/Matrix | Low |
| Prompt Report | Report with user-defined filters | Report with Slicers | Low |
| Derived Metric Report | Metrics calculated from other metrics | Measure (DAX) | Medium |
| Compound Metric | Multi-step metric calculations | Complex DAX Measure | High |
| Shortcut Report | Reference to existing report with filters | Bookmarks/Variants | Low-Medium |

### Metric Types & Calculation Rules

```
Simple Metric:
  Definition: Single aggregate function (SUM, COUNT, AVG, etc.)
  Example: Metric "Total Sales" = Sum(Revenue)
  Power BI: MEASURE = SUM('Sales'[Revenue])

Compound Metric:
  Definition: Metric referencing other metrics
  Example: Metric "Revenue Growth %" = (Current Year Sales / Previous Year Sales) - 1
  Power BI: Complex DAX with CALCULATE() and time intelligence functions

Derived Metric:
  Definition: Metric with conditions/filters applied
  Example: Metric "H1 Sales" = Sum(Revenue) Where Half = "H1"
  Power BI: CALCULATE(SUM(...), FILTER(...))
```

### Dimensional Hierarchy Patterns

```
Standard Hierarchy:
  Level 1: Country → Level 2: State → Level 3: City
  Power BI: Create Hierarchy in dimension table

Parent-Child Hierarchy:
  Uses Employee-Manager relationship, not levels
  Power BI: Use Path() function or denormalize to levels

Ragged Hierarchy:
  Missing levels in some branches
  Power BI: Use calculated columns with IF logic or denormalize

Shared Attributes:
  One attribute belongs to multiple dimensions
  Power BI: Create shared dimension or bridge table
```

### Security Model Patterns

```
Element-Level Security:
  Control which attribute values users see
  Example: Salesperson only sees their region
  Power BI RLS: [Region] = USERNAME() context

Metric-Level Security:
  Control which metrics users can access
  Power BI: Use Row-Level Security with metric filtering

Hierarchy Security:
  Control visibility at hierarchy levels
  Power BI: PATHS() function or RLS with hierarchy filtering
```

### Common MicroStrategy Functions & DAX Equivalents

| MicroStrategy | Purpose | Power BI DAX |
|---------------|---------|-------------|
| Sum() | Total of values | SUM() |
| Count() | Count of rows | COUNTROWS() |
| Avg() | Average value | AVERAGE() |
| Max() | Maximum value | MAX() |
| Min() | Minimum value | MIN() |
| Rank() | Ranking | RANKX() |
| RunningSum() | Cumulative total | Running SUM with CALCULATE |
| PercentOf() | Percentage calculation | DIVIDE(..., CALCULATE(...)) |
| YTD() | Year-to-date | DATESYTD() |
| MTD() | Month-to-date | DATESMTD() |
| PreviousPeriod() | Prior period | DATEADD(-1, ...) |

---

## 2. Power BI Semantic Model Design Patterns

### Star Schema Design

```
        ┌─────────────┐
        │   Date      │
        │  Dimension  │
        └────┬────────┘
             │
    ┌────────┼────────┐
    │        │        │
┌───▼───┐ ┌─┴─────┐ ┌─┴────────┐
│Product│ │ Sales │ │ Customer │
│Dim    │ │ Fact  │ │ Dim      │
└───────┘ └───────┘ └──────────┘
    │        │        │
    └────────┼────────┘
             │
        ┌────┴─────┐
        │ Geography│
        │Dimension │
        └──────────┘
```

### Table Design Principles

**Fact Tables:**
- Contain foreign keys to dimensions
- Contain measures (numeric data)
- Granularity clearly defined (daily, monthly, transaction-level)
- No descriptive attributes
- Typically narrow, tall (millions of rows)

**Dimension Tables:**
- Contain attributes for filtering/grouping
- Include hierarchies
- Slowly Changing Dimension (SCD) Type handling
- Typically wide, shorter (thousands of rows)
- 100:1 to 1000:1 fact-to-dimension ratio

### DAX Measure Patterns

**Basic Aggregation:**
```dax
Total Sales = SUM('Sales'[Amount])
```

**Aggregation with Filter:**
```dax
Current Year Sales = 
CALCULATE(
    SUM('Sales'[Amount]),
    'Date'[Year] = MAX('Date'[Year])
)
```

**Time Intelligence:**
```dax
Sales YTD = 
TOTALMTD(
    SUM('Sales'[Amount]),
    'Date'[DateKey]
)
```

**Ratio/Percentage:**
```dax
Sales Market Share % = 
DIVIDE(
    [Current Year Sales],
    CALCULATE([Current Year Sales], ALL('Customer'[Region])),
    0
)
```

**Complex Calculation:**
```dax
Revenue Growth % = 
VAR CurrentYearSales = [Current Year Sales]
VAR PreviousYearSales = 
    CALCULATE(
        SUM('Sales'[Amount]),
        DATEADD('Date'[DateKey], -1, YEAR)
    )
RETURN
    DIVIDE(
        CurrentYearSales - PreviousYearSales,
        PreviousYearSales,
        0
    )
```

---

## 3. Common Migration Challenges & Solutions

### Challenge 1: Complex Compound Metrics
**Problem:** MicroStrategy compound metrics with nested logic
**Solution:**
- Break into multiple intermediate measures
- Use variables (VAR) in DAX for clarity
- Test each component separately
- Document calculation order

### Challenge 2: Ragged/Unbalanced Hierarchies
**Problem:** Not all branches have same hierarchy levels
**Solution:**
- Denormalize to flat levels in Power BI
- Use explicit Path() function for parent-child
- Consider bridge tables for many-to-many relationships
- Document original structure for transparency

### Challenge 3: Alert/Threshold Logic
**Problem:** MicroStrategy alerts based on metric values
**Solution:**
- Create calculated columns for thresholds
- Use conditional formatting in reports
- Implement measures that return 0/1 for threshold logic
- Consider Power BI alerts feature for critical metrics

### Challenge 4: Large Data Volumes
**Problem:** Performance degradation with millions of rows
**Solution:**
- Use aggregation tables or DirectQuery for very large datasets
- Implement incremental refresh
- Create fact table subsets for frequently accessed data
- Use composite models (Import + DirectQuery)

### Challenge 5: Custom MicroStrategy Functions
**Problem:** Non-standard MicroStrategy functions with no DAX equivalent
**Solution:**
- Review business logic and recreate in DAX
- Consider Power Query transformations
- Use Python/R scripts within Power BI if needed
- Document original function behavior

### Challenge 6: Prompt/Filter Logic
**Problem:** Complex dynamic filters in MicroStrategy prompts
**Solution:**
- Translate to Power BI slicers and filters
- Use bookmark combinations for complex scenarios
- Consider Power BI parameters and what-if analysis
- Build filter UI with buttons and slicers

---

## 4. Data Source Connectivity Patterns

### Pattern 1: Direct Database Connection
```
MicroStrategy → SQL Server (Native)
Power BI → SQL Server (Power Query or DirectQuery)

Advantages: Direct access, minimal latency
Considerations: VPN/Gateway required, performance monitoring
```

### Pattern 2: Data Warehouse Connection
```
MicroStrategy → Data Warehouse → Reporting Layer
Power BI → Data Warehouse (Same source)

Advantages: Consistent data, centralized transformations
Considerations: Dependency on DW refresh, cost
```

### Pattern 3: Cloud Data Integration
```
MicroStrategy → Azure SQL / Synapse
Power BI → Azure SQL / Synapse (DirectQuery or Import)

Advantages: Scalability, cloud-native features
Considerations: Cloud costs, latency from MicroStrategy
```

### Pattern 4: Hybrid Approach
```
Fast-moving data → DirectQuery
Historical data → Import with refresh
Master data → Reference to static import

Total Query Time: <5 seconds
```

---

## 5. Row-Level Security (RLS) Implementation

### RLS Scenario 1: User-Based Security
```dax
-- Sales Manager sees only their region
'Sales'[Region] = LOOKUPVALUE(
    'UserMapping'[Region],
    'UserMapping'[Email],
    USERNAME()
)
```

### RLS Scenario 2: Department-Based Security
```dax
-- Finance team sees all departments
-- Operational team sees only their department
IF(
    USERNAME() IN {"Finance@company.com", "Controller@company.com"},
    TRUE(),
    'Department'[DeptName] = LOOKUPVALUE(
        'UserDept'[Department],
        'UserDept'[Email],
        USERNAME()
    )
)
```

### RLS Scenario 3: Hierarchical Security
```dax
-- Manager sees their team + their region
-- Individual contributor sees only themselves
IF(
    CONTAINS(
        'Security'[EmpID],
        'Security'[EmpID], USERNAME()
    ),
    TRUE(),
    AND(
        'Employee'[Region] = LOOKUPVALUE('UserSecurity'[Region], 'UserSecurity'[Email], USERNAME()),
        'Employee'[Manager] = LOOKUPVALUE('UserSecurity'[Manager], 'UserSecurity'[Email], USERNAME())
    )
)
```

---

## 6. Performance Optimization Checklist

- [ ] Data Types: Appropriate for column purpose (minimize DECIMAL, use INT for large ranges)
- [ ] Relationships: Marked correctly (1:*, active only where necessary)
- [ ] Hierarchies: Properly configured, no circular references
- [ ] Measures: Use CALCULATE() efficiently, avoid iterator functions in large fact tables
- [ ] Columns: Avoid unnecessary calculated columns (use measures instead)
- [ ] Aggregations: Defined for large fact tables
- [ ] Query Folding: Verified in Power Query transformations
- [ ] Partitions: Used for incremental refresh on large tables
- [ ] Caching: Row-level caching enabled on Premium capacity
- [ ] Peak Usage: Model tested under peak load conditions

---

## 7. Validation & Testing Framework

### Unit Testing: Individual Measures
```
Test: Total Sales Measure
Setup: Cube with Sales Fact table
Input: January 2024 data
Expected: 1,234,567
Power BI Result: 1,234,567
Status: ✓ PASS (Variance: 0%)
```

### Integration Testing: Multi-Measure Reports
```
Test: Sales Dashboard
Setup: 5 metrics, 4 filters
Input: Northeast region, 2024, Product X
Validation Points:
  - Revenue matches source: ✓
  - Unit count matches source: ✓
  - Margin calculation: ✓
  - YoY comparison: ✓
Status: ✓ PASS
```

### Security Testing: RLS
```
Test: Region-based RLS
Users Tested: 5 regional managers
Validation:
  - User_A (Northeast) sees 45 records: ✓
  - User_B (Southwest) sees 32 records: ✓
  - Admin sees all 150 records: ✓
  - Cross-region data hidden: ✓
Status: ✓ PASS
```

### Performance Testing: Query Response
```
Query: Complex metric with 3 filters
Target: <5 seconds
Result: 2.3 seconds
Load Test (10 concurrent users): 4.7 seconds (acceptable)
Status: ✓ PASS
```

---

## 8. Cutover & Rollback Procedures

### Pre-Cutover Checklist
- [ ] All measures validated (0% variance for critical metrics)
- [ ] Security testing complete (all RLS rules verified)
- [ ] Performance testing passed (<5 second response time)
- [ ] UAT sign-off obtained
- [ ] Backup of MicroStrategy environment created
- [ ] Backup of Power BI model created
- [ ] Communication sent to users (go-live time)
- [ ] Support team trained
- [ ] Rollback scripts prepared

### Cutover Execution Steps
1. Pause MicroStrategy scheduled refreshes (T-2 hours)
2. Final data sync and reconciliation
3. Execute final test run on Power BI (T-30 min)
4. Disable MicroStrategy access (T-0)
5. Redirect users to Power BI reports
6. Monitor for issues (continuous, 24 hours)
7. Document any discrepancies
8. Run UAT validation queries

### Rollback Procedures
1. Identify issue requiring rollback
2. Notify stakeholders within 15 minutes
3. Switch users back to MicroStrategy
4. Investigate root cause
5. Document issue and remediation
6. Re-execute cutover when issue resolved
7. Run full reconciliation

---

## 9. Maintenance & Ongoing Operations

### Daily Tasks
- Monitor refresh success in Power BI Service
- Check for user-reported issues
- Verify data accuracy spot-checks

### Weekly Tasks
- Review performance metrics
- Check gateway health (if on-premises)
- Validate security context for sample users

### Monthly Tasks
- Performance trend analysis
- User adoption metrics
- Identified optimization opportunities
- Documentation updates

### Quarterly Tasks
- Comprehensive audit of calculations
- Security rule review
- Capacity planning assessment
- Training needs assessment

