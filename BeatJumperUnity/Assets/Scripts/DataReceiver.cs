using System;
using System.Net;
using System.Net.Sockets;
using System.IO;
using UnityEngine;


public class DataReceiver : MonoBehaviour
{
    public string serverIP = "127.0.0.1"; 
    public int port = 8001;
    TcpListener server;
    TcpClient client;

    public GameObject ModelManager;

    public void StartReceiving()
    {
        try
        {
            // Establece la conexión
            server = new TcpListener(IPAddress.Parse(serverIP), port);
            server.Start();
            client = server.AcceptTcpClient();
            NetworkStream stream = client.GetStream();

            // Recibe los datos de tempo
            byte[] tempoBytes = new byte[4];
            stream.Read(tempoBytes, 0, tempoBytes.Length);
            float tempo = BitConverter.ToSingle(tempoBytes, 0);

            // Recibe la longitud del array de energía
            byte[] energyLengthBytes = new byte[4];
            stream.Read(energyLengthBytes, 0, energyLengthBytes.Length);
            int energyLength = BitConverter.ToInt32(energyLengthBytes, 0);

            // Recibe los datos de energía
            byte[] energyBytes = new byte[sizeof(float) * energyLength];
            stream.Read(energyBytes, 0, energyBytes.Length);
            float[] energy = new float[energyLength];
            Buffer.BlockCopy(energyBytes, 0, energy, 0, energyBytes.Length);

            // Cierra la conexión
            stream.Close();
            client.Close();
            server.Stop(); // Detener el TcpListener

            Debug.Log("Tempo recibido: " + tempo);
            Debug.Log("Energía recibida: " + string.Join(", ", energy));

            // Líneas de depuración adicionales para verificar los datos recibidos
            Debug.Log("tempoBytes recibidos: " + BitConverter.ToString(tempoBytes));
            Debug.Log("energyLengthBytes recibidos: " + BitConverter.ToString(energyLengthBytes));
            Debug.Log("energyBytes recibidos: " + BitConverter.ToString(energyBytes));

            ModelRunner modelScript = ModelManager.GetComponent<ModelRunner>();

            // Después de recibir los datos, pasa los datos al ModelRunner
            modelScript.ProcessData(tempo, energy);
        }
        catch (Exception e)
        {
            Debug.LogError("Error al recibir datos de audio: " + e.Message);
        }
    }
}