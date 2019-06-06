#!bin/bash
# header-info
header=$(echo -n '{"typ":"JWT","alg":"HS256","kid":"0001"}' | base64 | sed s/\+/-/ | sed -E s/=+$//)

# payload-info
payload=$(echo -n '{"name":"Quotation System","sub":"alice","iss":"My API Gateway"}' | base64 | sed s/\+/-/ | sed -E s/=+$//)

#concatenate header and payload to HEADER_PAYLOAD
HEADER_PAYLOAD="$header.$payload"
printf -v HEADER_PAYLOAD '%s' $HEADER_PAYLOAD

#sign the header and payload with symmetric key and encode the signature
signature=$(echo -n $HEADER_PAYLOAD | openssl dgst -sha256 -hmac fantasticjwt -binary | openssl base64 -e -A | sed s/\+/-/ | sed -E s/=+$//)

# append the encoded signature
sudo sh -c "echo $HEADER_PAYLOAD.$signature > token.jwt"
echo $HEADER_PAYLOAD.$signature
