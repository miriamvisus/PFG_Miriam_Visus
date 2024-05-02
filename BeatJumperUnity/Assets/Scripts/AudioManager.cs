using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AudioManager : MonoBehaviour
{
    void Start()
    {
        // Obtén referencias a los componentes AudioSender y DataReceiver
        AudioSender audioSender = GetComponent<AudioSender>();
        DataReceiver dataReceiver = GetComponent<DataReceiver>();

        // Asegúrate de que AudioSender envíe los datos antes de que DataReceiver los reciba
        StartCoroutine(SendAudioThenReceive(audioSender, dataReceiver));
    }

    IEnumerator SendAudioThenReceive(AudioSender sender, DataReceiver receiver)
    {
        // Inicia la secuencia de envío y recepción
        yield return StartCoroutine(sender.SendAudioData());
        
        // Comienza la recepción si el envío fue exitoso
        receiver.StartReceiving();
    }
}
