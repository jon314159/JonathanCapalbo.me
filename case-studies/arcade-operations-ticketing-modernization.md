# Arcade Operations Ticketing Modernization

## Portfolio disclosure

I designed a ticketing process for one fictional arcade. I wrote the requirements, user stories, acceptance tests and rollout materials. The people, operating data and targets are part of the scenario. The project ended at planning, before anyone built or deployed a system or measured results.

## Business problem

In the scenario, a staff member might call in a machine failure, leave a paper note about a refund or mention a game-card problem to the next shift. Prize-counter and facility issues can come in through any of the same channels. The shift lead has to piece together what is urgent, who owns it and whether anyone checked the fix.

## Recommended scope

I proposed one internal ticket for all five types of issues at one location. The shift lead would use category and urgency to assign work. The ticket would record approvals, changes of status and the final verification, giving managers a consistent record for reporting. Staff would address an immediate hazard before entering a ticket.

## Planning coverage

The case study follows a machine repair that fails verification. The supporting documents show how I connected the workflow to ten proposed requirements, user stories, acceptance criteria and fourteen planned user acceptance tests. The review roles are my assumptions for this exercise. All tests have the status **Not Executed**. [Read the case study](https://jonathancapalbo.me/arcade-ticketing-modernization.html) · [Open the requirements and test plan](https://jonathancapalbo.me/arcade-ticketing-evidence.html)

- Problem statement, project charter, stakeholder analysis, and scope
- Simulated current-state and proposed future-state workflows
- Functional, data, reporting, security, and nonfunctional requirements
- User stories and Given/When/Then acceptance criteria
- Data definitions and cross-field validation rules
- Requirements traceability and UAT planning
- Implementation and cutover plan, employee procedure, and governance model
- Definitions for the measures used in reports

## Proposed lifecycle

Staff would open a ticket once it was safe to do so. The shift lead would confirm priority and assign a named owner. A refund would stay In Progress while a manager decides. If a repair had to wait, the owner would record the reason and review date. After a repair, the shift lead would verify it before closure or send it back to the owner if it failed.

## ServiceNow positioning

I used ServiceNow’s documentation to see where the proposed process might fit. An interruption could be an incident, a staff request could go through the catalog, and a repair could use a work order. I also reviewed workplace services for facility issues. Before implementation, the team would need to check these assumptions with staff and the platform owner, review licensing, security and privacy, design the integrations, configure the system and test it.

## Methods and sources

- [The Business Analysis Standard (IIBA)](https://www.iiba.org/knowledgehub/the-business-analysis-standard/)
- [Gherkin Reference (Cucumber)](https://cucumber.io/docs/gherkin/reference/)
- [Incident Management (ServiceNow)](https://www.servicenow.com/products/incident-management.html)
- [Using the Service Catalog (ServiceNow)](https://www.servicenow.com/docs/r/servicenow-platform/service-catalog/c_UsingTheServiceCatalog.html)
- [Work orders in Field Service Management (ServiceNow)](https://www.servicenow.com/docs/r/field-service-management/Work-order-fsm.html)
- [Workplace Service Delivery (ServiceNow)](https://www.servicenow.com/products/workplace-service-delivery.html)
