const { default: makeWASocket, useSingleFileAuthState } = require('@whiskeysockets/baileys')
const { Boom } = require('@hapi/boom')
const fs = require('fs')

const number = process.argv[2]
const message = process.argv[3]

const { state, saveState } = useSingleFileAuthState('./auth.json')

async function start() {
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: true,
    })

    sock.ev.on('creds.update', saveState)

    await new Promise(resolve => setTimeout(resolve, 1000)) // wait for connection

    await sock.sendMessage(number + "@s.whatsapp.net", { text: message })
    console.log("Message sent to", number)
    process.exit(0)
}

start()
