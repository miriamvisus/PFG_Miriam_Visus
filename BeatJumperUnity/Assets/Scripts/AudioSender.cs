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
        // Carga el archivo de audio
        AudioClip audioClip = GetComponent<AudioSource>().clip;
        float[] audioData = new float[audioClip.samples * audioClip.channels];
        audioClip.GetData(audioData, 0);

        // Establece la conexión
        TcpClient client = new TcpClient(serverIP, port);
        NetworkStream stream = client.GetStream();

        // Envía el tamaño del archivo de audio
        byte[] sizeBytes = System.BitConverter.GetBytes(audioData.Length);
        stream.Write(sizeBytes, 0, sizeBytes.Length);

        Debug.Log("Tamaño del archivo de audio enviado: " + audioData.Length + " bytes");

        // Envía los datos de audio
        int totalBytesSent = 0;
        foreach (float sample in audioData)
        {
            byte[] sampleBytes = System.BitConverter.GetBytes(sample);
            stream.Write(sampleBytes, 0, sampleBytes.Length);
            totalBytesSent += sampleBytes.Length;
        }

        Debug.Log("Total de bytes de audio enviados: " + totalBytesSent + " bytes");

        // Cierra la conexión
        stream.Close();
        client.Close();
    }
}