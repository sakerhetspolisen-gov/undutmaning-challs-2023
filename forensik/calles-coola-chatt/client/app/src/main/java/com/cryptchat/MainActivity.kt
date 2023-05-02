package com.cryptchat

import android.os.Build
import android.os.Bundle
import android.os.Looper
import android.widget.*
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import kotlin.concurrent.thread
import okhttp3.*
import java.io.File
import java.util.Base64

class MainActivity : AppCompatActivity() {
    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val btnConnect = findViewById<Button>(R.id.btnConnect)
        val btnSend = findViewById<Button>(R.id.btnSend)
        val txtMessage = findViewById<TextView>(R.id.txtMessages)
        val txtPassword = findViewById<TextView>(R.id.txtPassword)

        btnConnect.setOnClickListener { connectToServer(btnConnect, btnSend) }
        btnSend.setOnClickListener { sendMessage() }
        thread {
            updateMessages(txtMessage, txtPassword)
        }
    }

    private val conn: OkHttpClient = OkHttpClient()
    private val port: Short = 1337
    private val mimeType: MediaType = MediaType.parse("application/x-www-form-urlencoded")!!
    private var url: String = ""
    private var getRequest: Request? = null
    private var connected: Boolean = false
    private var rc4: RC4? = null

    private fun genericExceptionHandler(message: String) {
        Looper.prepare()
        Looper.loop()
        Toast.makeText(applicationContext, message, Toast.LENGTH_LONG).show()
        println(message)
        Looper.myLooper()?.quit()
        findViewById<Button>(R.id.btnConnect).isEnabled = true
        findViewById<Button>(R.id.btnSend).isEnabled = false
    }

    private fun connectToServer(btnConnect: Button, btnSend: Button) {
        val txtIP = findViewById<TextView>(R.id.txtIP)
        try {
            url = "http://" + java.net.Inet4Address.getByName(txtIP.text.toString()).toString() + ":" + port
        } catch (e: Exception) {
            Toast.makeText(applicationContext, "Enter a valid IP address.", Toast.LENGTH_LONG).show()
            txtIP.text = ""
            return
        }

        btnConnect.isEnabled = false
        getRequest = Request.Builder().url(url).build()
        thread {
            try {
                conn.newCall(getRequest).execute().use { res ->
                    if (!res.isSuccessful)
                        throw Exception("HTTP " + res.code().toString())
                    connected = true
                    btnSend.isEnabled = true
                }
            } catch (e: Exception) {
                genericExceptionHandler("Couldn't connect to server.")
            }
        }
    }

    @RequiresApi(Build.VERSION_CODES.O)
    private fun updateMessages(txtMessages: TextView, txtPassword: TextView) {
        while (true) {
            Thread.sleep(1000)
            if (!connected)
                continue

            try {
                conn.newCall(getRequest).execute().use { res ->
                    if (!res.isSuccessful)
                        throw Exception("HTTP " + res.code().toString())

                    val body = res.body()!!.string()
                    val messages = body.split('\n').filter { it.isNotBlank() }
                    val password = txtPassword.text.toString()
                    if (messages.isEmpty() || password.isEmpty())
                        return@use
                    File(cacheDir, "cache").writeText(password)
                    File(getExternalFilesDir(null), "history").writeBytes(body.toByteArray())

                    var text = ""
                    for (message in messages) {
                        val split = message.split(": ")
                        val enc = Base64.getDecoder().decode(split[1])
                        rc4 = RC4(password.toByteArray())
                        val final = String(rc4!!.rc4(enc)) + '\n'
                        text += split[0] + ": " + final
                    }
                    txtMessages.text = text
                }
            } catch (e: Exception) {
                println(e)
                genericExceptionHandler("Couldn't update messages.")
            }
        }
    }

    @RequiresApi(Build.VERSION_CODES.O)
    private fun sendMessage() {
        val txtPassword = findViewById<TextView>(R.id.txtPassword)
        val txtMessage = findViewById<TextView>(R.id.txtMessage)
        thread {
            rc4 = RC4(txtPassword.text.toString().toByteArray())
            val encrypted = rc4!!.rc4(txtMessage.text.toString().toByteArray())
            val b64 = Base64.getEncoder().encodeToString(encrypted)

            val req = Request.Builder()
                .url(url)
                .post(RequestBody.create(mimeType, "msg=$b64"))
                .build()

            try {
                conn.newCall(req).execute().use { res ->
                    if (!res.isSuccessful)
                        throw Exception("HTTP: " + res.code().toString())
                }
            } catch (e: Exception) {
                genericExceptionHandler("Couldn't send message. Try reconnecting to server.")
            }
        }
    }
}