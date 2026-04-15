from Crypto.Hash import SHA256
vec = b'LoremipsumdolorsitametconsecteturadipiscingelitseddoeiusmodtemporincididuntutlaboreetdoloremagnaaliquaUtenimadminimveniamquisnostrudexercitationullamcolaborisnisiutaliquipexeacommodoconsequatDuisauteiruredolorinreprehenderitinvoluptatevelitessecillumdoloreeufugiatnullapariaturExcepteurs.'
tmp = [vec[i:i+16] for i in range(0, len(vec), 16)]
print(tmp)
ans = b''
for t in tmp:
    ans += t[15:16]
print(ans)
print(SHA256.new(data=ans).hexdigest())