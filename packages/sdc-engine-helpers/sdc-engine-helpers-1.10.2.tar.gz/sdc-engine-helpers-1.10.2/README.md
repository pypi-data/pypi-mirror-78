# SDC Engine Helpers Package
![Test Recommendations](https://github.com/RingierIMU/sdc-recommend-engine-helpers/workflows/Test%20Recommendations/badge.svg)
![Test Events](https://github.com/RingierIMU/sdc-recommend-engine-helpers/workflows/Test%20Events/badge.svg)
![Test Mainteneance](https://github.com/RingierIMU/sdc-recommend-engine-helpers/workflows/Test%20Mainteneance/badge.svg)
![Tests](https://github.com/RingierIMU/sdc-recommend-engine-helpers/workflows/Tests/badge.svg)
### Description

Helper modules for interacting with Recommendation Engine services based on AWS infrastructure.

### Requirements

- Redis-cli
- mysql client

### Quick Setup

1. Create a .env file and add the following:

```
DB_DATABASE='sdc'
REDIS_HOST='/your/redis/host'
REDIS_PORT=6379
RDS_HOST='/your/mysql/host'
RDS_USERNAME='/your/mysql/username'
RDS_PORT=3306
RDS_PASSWORD='/your/password/'
RDS_DB_NAME='/your/default/schema'
```

2. Run the `Makefile`:

```
make build
```

## Helpers

General functions to get key components out of subscriptions properties/engine

Currently available:

`get_engine` - Get an engine out of the client's subscription properties passing the engine's slug as a parameter.

`get_dataset` - Get a dataset of out of an engine's data using a dataset label.

`get_campaign` - Get a campaign out an engine either using the campaign's arn or by passing the recipe and optionally, 
the event_type.

`get_solution` - Get a campaign out an engine either using the campaign's arn or by passing the recipe and optionally, 
the event_type.

`update_dataset` - Update a dataset for an engine's given the dataset label.

`update_campaign` - Update a campagn for an engine either using the campaign's arn or by passing the recipe and optionally, 
the event_type.

`update_solution` - Update a solution for an engine either using the solution's arn or by passing the recipe and optionally, 
the event_type.

## Available Engine Helpers

### Maintenance

The purpose of this module is to help ensure that Recommendation Engine solution versions
are created when required so that the latest tracked data is taken into account
for recommendation inferences.

When solution versions are ready, the campaigns (inference endpoints) are updated
to use the latest solution version.

The above actions are controlled by scheduling fields stored in our database i.e
frequency and next action times. We also ensure that statuses are kept in sync between 
the database and what they are in the Recommendation Engine.

#### Code Analysis

| Class                | Description   |    
| -------------------- | ------------- |  
| MaintenanceManager   | For all active clients in the database, create Recommendation Engine solution version and/or update Recommendation Engine campaigns if the Recommendation Engine state has changed. The core functionality involves managing the database state through calling each of the state managers in turn.|
| SolutionStateManager | Given a solution defined in the database, determine whether it is time to create a new solution version or to sync the Recommendation Engine status with the database status. The core functionality involves calling AWS API's to either get_state or update_state in AWS. Finally, returning a config or state object to the maintenance manager to update the database. |
| CampaignStateManager | Given a campaign defined in the database, determine whether it is time to update a campaign or to sync the Recommendation Engine status with the database status.  The core functionality involves calling AWS API's to either get_state or update_state in AWS. Finally, returning a config or state object to the maintenance manager to update the database. |
| DatasetStateManager | Given a dataset defined in the database, determine whether it is time to update the dataset. The core functionality involves calling AWS API's to either get_state or update_state in AWS. Finally, returning a config or state object to the maintenance manager to update the database. |

### Event

The purpose of this module is to track real-time events to AWS Recommendation Engine

#### Code Analysis

| Class        | Description   |    
| -------------| ------------- |  
| EventManager | For a given client, determine the Recommendation Engine event tracking id from the database and track an event for the given item id and user id

### Recommendations

The purpose of this module is to provide recommendations from AWS Recommendation Engine campaigns

#### Code Analysis

| Class                  | Description   |    
| ---------------------- | ------------- |  
| RecommendationsManager | For a given client, determine the Recommendation Engine campaign from the database and provide recommendations for the given item id