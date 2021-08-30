#!/bin/bash

curl "http://localhost:8000/books/${ID}/" \
  --include \
  --request DELETE \
  --header "Authorization: Token ${TOKEN}"

echo
