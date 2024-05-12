# 1. Telegram login

When a user opens a webapp in Telegram, it will post a basic user info to server.
If the user exists in DB, it will return user related infomation.
If the user does not exist in DB, the server will create a user record in DB and return user related infomation.

BTW, in the future, we perhaps need more user related infomation like: wallet address, token count, nft..

**URL** : `/api/tg/login`
**Method** : `POST`
**Auth required** : NO

### Request

```json
{
  "tg_id": "819829010",
  "first_name": "abc",
  "last_name": "efg",
  "username": "ghfff",
  "language_code": "zh-hans"
}
```

### Response

**Code** : `200 OK`

```json
{
  "tg_id": "819829010",
  "first_name": "abc",
  "last_name": "efg",
  "language_code": "zh-hans"
}
```

### Error Response

**Condition** : If 'username' and 'password' combination is wrong.
**Code** : `400 BAD REQUEST`

```json
{
  "errors": {
    "info": "System error or something"
  }
}
```

# 2. Others
