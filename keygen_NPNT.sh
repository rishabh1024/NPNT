openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -outform PEM -pubout -out public.pem
openssl req -new -key private.pem -out certificate.csr

openssl x509 -req -days 365 -in certificate.csr -signkey private.pem -out certificate.crt
