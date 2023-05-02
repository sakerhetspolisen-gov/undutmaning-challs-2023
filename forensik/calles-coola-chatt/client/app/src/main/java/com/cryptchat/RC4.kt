package com.cryptchat

import kotlin.experimental.xor

/**
 * RC4
 * This class implements the RC4 algorithm
 *
 * After generating the encrypted text [s] needs to be regenerated via [reset]
 *
 * @param key encryption key
 *
 * @version 1.0
 * @author MalteSchwitters
 * @author fluktuid
 *
 */

class RC4 internal constructor(private val key: ByteArray) {
    private val s = ByteArray(256)

    init {
        if (key.isEmpty() || key.size > 256) {
            throw IllegalArgumentException("key length must be between 1 and 256")
        } else {
            initializeS()
        }
    }

    private fun initializeS() {
        val t = ByteArray(256)
        for (i in 0..255) {
            s[i] = i.toByte()
            t[i] = key[i % key.size]
        }
        var j = 0
        var tmp: Byte
        for (i in 0..255) {
            j = j + s[i].toInt() + t[i].toInt() and 0xFF
            tmp = s[j]
            s[j] = s[i]
            s[i] = tmp
        }
    }

    /**
     * resets [s]
     */
    private fun reset() = initializeS()

    /**
     * encrypt the text with the generated [s]
     *
     * @param plaintext the byte array to encrypt
     * @return the encrypted byte array
     */
    fun rc4(plaintext: ByteArray): ByteArray {
        val cipherText = ByteArray(plaintext.size)
        var i = 0
        var j = 0
        var k: Byte
        var t: Int
        var tmp: Byte
        for (counter in plaintext.indices) {
            i = i + 1 and 0xFF
            j = j + s[i] and 0xFF
            tmp = s[j]
            s[j] = s[i]
            s[i] = tmp
            t = s[i] + s[j] and 0xFF
            k = s[t]
            cipherText[counter] = (plaintext[counter] xor k)
        }
        return cipherText
    }
}