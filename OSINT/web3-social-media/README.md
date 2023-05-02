# WEB3 Social Media 

## 1.1 Description

A warmup social media CTF using some of the web 3.0 social media platforms: 

* mastodon.nu
* odysee.com 

## 1.2 Public description

`Web 3.0`

## 1.3 Build

N/A

## 1.4 Story

```
Vi misstänker att en ondsint sockerbagare har kommit över någon av Haralds topphemliga smaktillsatser. Vi tror att hen 
försöker föra ut information till annat land. Vi måste få reda på vilken information hen har kommit över för att 
kunna göra en korrekt medbedömning. `#ensockerbagare #twitteralternative #web3 #sverige`
```

## 1.5 How to solve

1. The user gets the hint `#ensockerbagare #twitteralternative #web3 #sverige`
2. The Mastodon account hosted on the Swedish server `mastodon.nu` (The CTF user must guess the correct "Swedish" server).
The account `@ensockerbagare` has one post with a stereogram image with the text `ODYSEE`. The user gets a 
text hint saying `Stork, David G. and Rocca, Chris (1989). Sändning sker på andra kanalen!`. 
3. The Odysee account for `@ensockerbagare` has one posted video with a numbers station that transmits hex encoded text 
in morse code. The user can either decode it by hand (difficult) or record the morse sound and decode it using sites as
https://morsecode.world/international/decoder/audio-decoder-adaptive.html and then decode the ascii hex with sites like
https://www.rapidtables.com/convert/number/ascii-to-hex.html
4. The flag is `undut{RsO2cmJyeXRhcmVuIFPDtnJqYW4gU3VyZGVnIMOkciBoYXJhbGRzIHbDpHJzdGEgZm}`.

## 1.6 Solutions scripts

N/A

## 1.7 Level

Easy

## 1.8 Hints

https://joinmastodon.org/servers

## Accounts 

* The Mastodon account
  * URL: mastodon.nu
  * User: 
  * Pass:

* The Odysee account
  * URL:
  * User:
  * Pass:
