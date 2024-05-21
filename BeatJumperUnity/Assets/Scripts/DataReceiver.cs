using System;
using System.Net;
using System.Net.Sockets;
using System.Collections;
using System.Collections.Generic;
using System.Threading;
using UnityEngine;
using PimDeWitte.UnityMainThreadDispatcher;


public class DataReceiver : MonoBehaviour
{
    Thread thread;
    public string serverIP = "127.0.0.1"; 
    public int port = 8001;
    TcpListener server;
    bool running;

    public ModelRunner modelRunner;

    public delegate void DataReceived(float tempo, float[] energy);
    public static event DataReceived OnDataReceived;

    private float tempo;
    private float[] energy;
    private int energyLength;

    void Start()
    {
        modelRunner = GetComponent<ModelRunner>();
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
                if (!server.Pending()) // Espera hasta que haya un cliente
                {
                    Thread.Sleep(100); // Evitar el uso excesivo de CPU
                    continue;
                }

                using (TcpClient client = server.AcceptTcpClient())
                {
                    Debug.Log($"Servidor escuchando en {serverIP}:{port}");
                    Connection(client);
                }
            }
        }
        catch(Exception ex)
        {
            Debug.LogError("Error al recibir datos de audio: " + ex.Message);
        }
        finally
        {
            if (server != null)
            {
                server.Stop();
            }
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

            UnityMainThreadDispatcher.Instance().Enqueue(() => OnDataReceived?.Invoke(tempo, energy));

            UnityMainThreadDispatcher.Instance().Enqueue(() => modelRunner.ProcessData(tempo, energy));
        }
        
        catch (Exception ex)
        {
            Debug.LogError("Error al recibir datos de audio: " + ex.Message);
        }
    }

    void OnDestroy()
    {
        running = false;
        if (thread != null && thread.IsAlive)
        {
            thread.Join();
        }
        if (server != null)
        {
            server.Stop();
        }
    }
}