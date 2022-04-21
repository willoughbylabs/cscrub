# Cscrub API Usage

Please note: This project is currently being built. Swagger documentation and all features are not yet operational in this build.</br>

## Endpoints

### Meetings
`/api/meetings` </br>
`/api/meetings?year=2021`
```
meetings: [
    {
    id
    type
    date
    time
    link
    },
    ...
]
```

### Members (Alderpersons)
`/api/members`
```
members: [
    {
    id
    name
    },
    ...
]
```

### Legislation
`/api/legislation`</br>
`/api/legislation?date=3%2F16%2F2022`
```
legislation: [
    {
    id
    record_num
    type
    title
    result
    action_text
    mtg_date
    },
    ...
]
```

### Votes
`/api/votes`</br>
`/api/votes?member={member_id}`</br>
`/api/votes?record={record_num}`
```
votes: [
    {
    id
    record_num
    title
    member_name
    vote
    },
    ...
]
```
