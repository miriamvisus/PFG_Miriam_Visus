using System;
using System.Net;
using System.Net.Sockets;
using UnityEngine;
using System.Threading;


public class DataReceiver : MonoBehaviour
{
    Thread thread;
    public string serverIP = "127.0.0.1"; 
    public int port = 8001;
    TcpListener server;
    bool running;

    public GameObject ModelManager;

    public delegate void DataReceivedHandler(float tempo, float[] energy, int energyLength);
    public static event DataReceivedHandler OnDataReceived;

    private float tempo;
    private float[] energy;
    private int energyLength;

    void Start()
    {
        thread = new Thread(ReceiveData);
        thread.Start();
    }

    void ReceiveData()
    {
        try 
        {
            server = new TcpListener(IPAddress.Parse(serverIP), port);
            server.Start();

            running = true;
            while (running)
            {
                TcpClient client = server.AcceptTcpClient();
                Debug.Log($"Servidor escuchando en {serverIP}:{port}");
                Connection(client);
                client.Close();
            }

            server.Stop();
        }

        catch(Exception ex)
        {
            Debug.LogError("Error al recibir datos de audio: " + ex.Message);
        }
    }

    void Connection(TcpClient client)
    {
        try
        {
            NetworkStream stream = client.GetStream();

            byte[] tempoBytes = new byte[4];
            stream.Read(tempoBytes, 0, tempoBytes.Length);
            tempo = BitConverter.ToSingle(tempoBytes, 0);

            byte[] energyLengthBytes = new byte[4];
            stream.Read(energyLengthBytes, 0, energyLengthBytes.Length);
            energyLength = BitConverter.ToInt32(energyLengthBytes, 0);

            byte[] energyBytes = new byte[sizeof(float) * energyLength];
            stream.Read(energyBytes, 0, energyBytes.Length);
            energy = new float[energyLength];
            Buffer.BlockCopy(energyBytes, 0, energy, 0, energyBytes.Length);

            Debug.Log("Tempo recibido: " + tempo);
            Debug.Log("Energía recibida: " + string.Join(", ", energy));

            // Invoca el evento para notificar que los datos han sido recibidos
            OnDataReceived?.Invoke(tempo, energy, energyLength);
        }
        
        catch (Exception ex)
        {
            Debug.LogError("Error al recibir datos de audio: " + ex.Message);
        }
    }

    void OnDestroy()
    {
        running = false;
        thread.Join();
    }
}


public class MainClass : MonoBehaviour
{
    private DataReceiver dataReceiver;

    void Start()
    {
        dataReceiver = GetComponent<DataReceiver>();
        DataReceiver.OnDataReceived += HandleDataReceived;
    }

    void HandleDataReceived(float tempo, float[] energy, int energyLength)
    {
        // Aquí puedes acceder a los elementos del hilo principal
        ModelRunner modelRunner = dataReceiver.ModelManager.GetComponent<ModelRunner>();
        modelRunner.ProcessData(tempo, energy, energyLength);
    }

    void OnDestroy()
    {
        DataReceiver.OnDataReceived -= HandleDataReceived;
    }
}