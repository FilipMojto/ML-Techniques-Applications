
# Risk assessment

## Security risks

There are several risks using our API:

1) No real authorization for user accounts
2) ORM not integrated - raw queries are used

### Operational risks

1) Multiple concurrent requests may cause database locking issues
