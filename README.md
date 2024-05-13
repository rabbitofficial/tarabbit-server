## API Documentation

### 1. Check My Fortune

**URL:** `/check-my-fortune`

**Method:** `POST`

**Description:** This endpoint is used to get the user's fortune based on the Tarot reading. The fortune is generated by sending a prompt, composed of the provided Tarot cards, to the OpenAI GPT-3.5 model and formatting the model's response into a string.

**Request:**

```json
{
  "userId": "123456",
  "tarotCards": ["The Fool", "The Magician", "The High Priestess"]
}
```

**Response:**

**Code** : `200 OK`

```json
{
  "fortune": "The Fool represents new beginnings, The Magician represents manifestation, and The High Priestess represents intuition and mystery. Together, they suggest a journey of self-discovery and personal growth."
}
```

**Request Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `userId` | String | The unique identifier of the user. |
| `tarotCards` | Array of Strings | The list of Tarot cards for the reading. |

**Response Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `fortune` | String | The fortune telling result based on the Tarot reading. The fortune is a combined interpretation of all the Tarot cards provided in the request, generated by the OpenAI GPT-3.5 model. |

### 2. Telegram login

**URL:** `/api/tg/login`

**Method:** `POST`

**Description:** When a user opens a webapp in Telegram, it will post basic user info to the server. If the user exists in the database, it will return user-related information. If the user does not exist in the database, the server will create a user record in the database and return user-related information.

BTW, in the future, we perhaps need more user related infomation like: wallet address, token count, nft..


**Request:**

```json
{
  "tg_id": "819829010",
  "first_name": "abc",
  "last_name": "efg",
  "username": "ghfff",
  "language_code": "zh-hans"
}
```

**Response:**

**Code** : `200 OK`

```json
{
  "tg_id": "819829010",
  "first_name": "abc",
  "last_name": "efg",
  "language_code": "zh-hans"
}
```

**Error Response:**

**Condition** : If 'username' and 'password' combination is wrong.
**Code** : `400 BAD REQUEST`

```json
{
  "errors": {
    "info": "System error or something"
  }
}
```

**Request Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `tg_id` | String | The unique identifier of the user in Telegram. |
| `first_name` | String | The first name of the user. |
| `last_name` | String | The last name of the user. |
| `username` | String | The username of the user in Telegram. |
| `language_code` | String | The language code of the user. |

**Response Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `errors` | Object | An object containing error information. |
| `errors.info` | String | A string describing the error. |