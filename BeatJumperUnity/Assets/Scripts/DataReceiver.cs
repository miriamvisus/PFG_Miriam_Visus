using System;
using System.Net;
using System.Net.Sockets;
using System.IO;
using UnityEngine;
using System.Threading;
using System.Text;


public class DataReceiver : MonoBehaviour
{
    Thread thread;
    public string serverIP = "127.0.0.1"; 
    public int port = 8000;
    TcpListener server;
    TcpClient client;
    bool running;

    public GameObject ModelManager;

    void Start()
    {
        // Receive on a separate thread so Unity doesn't freeze waiting for data
        ThreadStart ts = new ThreadStart(ReceiveData);
        thread = new Thread(ts);
        thread.Start();
    }

    void ReceiveData()
    {
        // Imprime por pantalla el mensaje indicando que el servidor está escuchando
        Debug.Log($"Servidor escuchando en {serverIP}:{port}");

        // Establece la conexión
        server = new TcpListener(IPAddress.Any, port);
        server.Start();
        client = server.AcceptTcpClient();

        // Start listening
        running = true;
        while (running)
        {
            Connection();
        }
        server.Stop();
    }

    void Connection()
    {
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


        Debug.Log("Tempo recibido: " + tempo);
        Debug.Log("Energía recibida: " + string.Join(", ", energy));

        ModelRunner modelScript = ModelManager.GetComponent<ModelRunner>();

        // Después de recibir los datos, pasa los datos al ModelRunner
        modelScript.ProcessData(tempo, energy);
    }
}