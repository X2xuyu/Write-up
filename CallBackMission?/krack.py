import binascii

# 1. ข้อความที่ถูกเข้ารหัสความยาว 47 bytes (Ciphertext 1)
# (นำค่า cipher จาก log ที่มีความยาว len=47 มาใส่)
cipher47 = binascii.unhexlify("ใส่ค่า_Ciphertext_ที่ยาว_47_ตรงนี้")

# 2. ข้อความจริงที่เราทราบจากคำใบ้ (Plaintext 1)
plain47 = b"GET /admin/settings/configuration.json HTTP/1.1"

# 3. คำนวณหา Keystream (Ciphertext 1 XOR Plaintext 1)
keystream = bytes([c ^ p for c, p in zip(cipher47, plain47)])

# 4. นำ Keystream ไปถอดรหัสแพ็กเก็ตความยาว 37 bytes (Ciphertext 2)
# (นำค่า cipher จาก log ที่มีความยาว len=37 มาใส่)
cipher37 = binascii.unhexlify("ใส่ค่า_Ciphertext_ที่ยาว_37_ตรงนี้")
flag = bytes([c ^ k for c, k in zip(cipher37, keystream)])

print("Decrypted Flag:", flag.decode())
