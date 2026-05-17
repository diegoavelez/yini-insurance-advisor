# Plan

1. PRD Contract Mapping
   - Map the PRD retrieval, response, and workflow state shapes into typed
     Pydantic models.
   - Keep the first pass limited to the fields already specified in the PRD.

2. Document and Tool Contracts
   - Add retrieval chunk, clause, comparison, and tool IO models.
   - Restrict enum-like fields to the approved values only.

3. Response and State Contracts
   - Add citation, verification, advisor response, and workflow state models.
   - Keep state explicit and reusable for future LangGraph work.

4. Public Contract Surface
   - Export the shared contracts from `contracts/__init__.py`.
   - Keep module boundaries clear so future code can import from stable paths.

5. Validation and Tests
   - Add tests for valid construction and invalid enum/category cases.
   - Verify the contracts express the PRD structure without extra speculative
     fields.
