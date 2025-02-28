# DB

## Tables

### Users

user_id (spotify login) | tournament_id | created_at | updated_at


### Tournaments

tournamnent_id | round | tournament_type | created_at | updated_at


### Round Submissions (append only table)

tournament_id | round_id | user_id | submission | created_at

### Round Votes - upvote/downvote (append only table)

tournament_id | round_id | user_id | submission | vote | created_at | updated


### Round Votes - ranked choice (append only table)

tournament_id | round_id | user_id | submission | rank | created_at | updated_at