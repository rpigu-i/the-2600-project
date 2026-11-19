#! /bin/bash
echo -en '{"token":"xx-xx-xx", "access_point_id":1234}' |
curl -ikX POST -H "Content-Type: application/json" -H "Connection: close" \
--data-binary @- https://portal.gatewise.com/api/v1/visitor/open_gate


