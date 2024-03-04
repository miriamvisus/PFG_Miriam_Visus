using System;
using System.Net.Sockets;
using UnityEngine;

public class UnityClient : MonoBehaviour
{
    public string serverAddress = "127.0.0.1";
    public int serverPort = 8888;

    private Socket clientSocket;

    void Start()
    {
        // Crea un socket TCP/IP
        clientSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

        // Conecta el socket al servidor Python
        clientSocket.Connect(serverAddress, serverPort);
    }

    void Update()
    {
        // Aquí deberías enviar los datos de audio al servidor Python
        // Por ejemplo, puedes enviar un búfer de audio en formato de bytes
        byte[] audioData = GetAudioData();
        clientSocket.Send(audioData);

        // Espera los resultados del análisis de audio desde el servidor Python
        byte[] buffer = new byte[1024];
        int bytesRead = clientSocket.Receive(buffer);
        string data = System.Text.Encoding.UTF8.GetString(buffer, 0, bytesRead);
        Debug.Log("Resultados del análisis de audio: " + data);
    }

    // Este método simula la obtención de datos de audio en Unity
    byte[] GetAudioData()
    {
        // Aquí deberías obtener y retornar los datos de audio en formato de bytes
        return new byte[1024];
    }

    void OnDestroy()
    {
        // Cierra el socket cuando el GameObject sea destruido
        clientSocket.Close();
    }
}
