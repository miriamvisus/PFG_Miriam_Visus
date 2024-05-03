using System;
using System.Net;
using System.Net.Sockets;
using System.IO;
using System.Collections;
using UnityEngine;


public class AudioSender : MonoBehaviour
{
    public string serverIP = "127.0.0.1"; 
    public int port = 8000; 

    void Start()
    {
        try
        {
            // Carga el archivo de audio
            AudioClip audioClip = GetComponent<AudioSource>().clip;
            float[] audioData = new float[audioClip.samples * audioClip.channels];
            audioClip.GetData(audioData, 0);

            // Establece la conexión
            TcpClient client = new TcpClient(serverIP, port);
            NetworkStream stream = client.GetStream();
            
            // Envía el tamaño del archivo de audio
            byte[] sizeBytes = BitConverter.GetBytes(audioData.Length);
            stream.Write(sizeBytes, 0, sizeBytes.Length);

            Debug.Log("Tamaño del archivo de audio enviado: " + audioData.Length + " bytes");

            // Envía los datos de audio en búferes de 1024 bytes
            int bufferSize = 1024;
            int totalBytesSent = 0;
            for (int i = 0; i < audioData.Length; i += bufferSize)
            {
                int bytesToSend = Math.Min(bufferSize, audioData.Length - i);
                byte[] buffer = new byte[bytesToSend * sizeof(float)];
                Buffer.BlockCopy(audioData, i * sizeof(float), buffer, 0, bytesToSend * sizeof(float));
                stream.Write(buffer, 0, buffer.Length);
                totalBytesSent += buffer.Length;
            }

                Debug.Log("Total de bytes de audio enviados: " + totalBytesSent + " bytes");
        }
        
        catch (Exception ex)
        {
            Debug.LogError("Error al enviar datos de audio: " + ex.Message);
        }
    }
}