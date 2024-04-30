using System;
using System.Net;
using System.Net.Sockets;
using System.IO;
using UnityEngine;


public class DataReceiver : MonoBehaviour
{
    public string serverIP = "127.0.0.1"; 
    public int port = 8888; 

    void Start()
    {
        // Establece la conexión
        TcpClient client = new TcpClient(serverIP, port);
        NetworkStream stream = client.GetStream();

        // Recibe los datos de tempo
        byte[] tempoBytes = new byte[4];
        stream.Read(tempoBytes, 0, tempoBytes.Length);
        float tempo = BitConverter.ToSingle(tempoBytes, 0);

        // Recibe los datos de energía
        int energyLength = 10; // Ajusta esto al tamaño real de los datos de energía
        byte[] energyBytes = new byte[sizeof(float) * energyLength];
        stream.Read(energyBytes, 0, energyBytes.Length);
        float[] energy = new float[energyLength];
        Buffer.BlockCopy(energyBytes, 0, energy, 0, energyBytes.Length);

        // Cierra la conexión
        stream.Close();
        client.Close();

        // Haz lo que quieras con los datos de tempo y energía
        Debug.Log("Tempo recibido: " + tempo);
        Debug.Log("Energía recibida: " + string.Join(", ", energy));
    }
}