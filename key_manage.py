#### KEY MANAGEMENT ####

""" generate private key : 'openssl genpkey -algorithm RSA -out rsa_private.pem -pkeyopt rsa_keygen_bits:2048'
	
	generate public key : 'openssl rsa -in rsa_private.pem -pubout -out rsa_public.pem'


	Get certficate out of the card

	$SIGN_KEY : signing key ID

	$PIN : card pin	

	./src/tools/pkcs11-tool -r -p $PIN --id $SIGN_KEY --type cert --module ./src/pkcs11/.libs/opensc-pkcs11.so > $SIGN_KEY.cert

	Get public key out of the card

	 ./src/tools/pkcs11-tool -r -p $PIN --id $SIGN_KEY --type pubkey --module ./src/pkcs11/.libs/opensc-pkcs11.so > $SIGN_KEY.der

	 and Now convert the key to PEM format

	 openssl rsa -inform DER -outform PEM -in $SIGN_KEY.der -pubin > $SIGN_KEY.pub
 


	Signing the public using PKCS11-tool :

	pkcs11-tool.exe --id 010100bf37c7a15f1b998273ed7cf88a19af7f40 -s -m SHA256-RSA-PKCS  --module "C:\\Windows\\System32\\Watchdata\\PROXKey CSP India V2.0\\wdpkcs.dll" ---input-file private.pem  --output-file pvt.sign

	--id : token id number

	-s : for signing

	-m : mechanism for signing

	--module : correspodning module for the PKI token i.e. watchdata in our case / it will be an so file for linux

	--input-file : file to be signed

	--output file : output signature file

	Verifying the signature at the USER end:

	openssl dgst -keyform PEM -verify 010100bf37c7a15f1b998273ed7cf88a19af7f40.pub -sha1 -signature pvt.sign private.pem

	Here pvt.sign and private.pem are verified with public key as input

"""


import os

