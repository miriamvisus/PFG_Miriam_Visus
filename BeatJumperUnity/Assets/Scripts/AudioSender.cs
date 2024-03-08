using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Net.Sockets;

public class AudioSender : MonoBehaviour
{
    public string serverAddress = "127.0.0.1";
    public int serverPort = 8888;
    public string audioFilePath;

    private TcpClient client;

    void Start()
    {
        client = new TcpClient();
        client.Connect(serverAddress, serverPort);

        // Llamar al método para enviar el archivo de audio al servidor
        SendAudioToServer(audioFilePath);
    }

    void SendAudioToServer(string filePath)
    {
        // Leer los datos del archivo de audio
        byte[] audioData = File.ReadAllBytes(filePath);

        // Enviar los datos de audio al servidor Python a través de sockets
        NetworkStream stream = client.GetStream();
        stream.Write(audioData, 0, audioData.Length);

        // Cerrar la conexión después de enviar los datos
        client.Close();
    }
}

