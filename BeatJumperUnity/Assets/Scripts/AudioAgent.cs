using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using Unity.MLAgents.Actuators;
using System.Collections;

public class AudioAgent : Agent
{
    // URL del modelo en GitHub
    public string modelUrl = "https://github.com/miriamvisus/PFG_Miriam_Visus_Martin/blob/main/BeatJumperPython/trained_model.keras";

    // Datos de entrada para el modelo
    private float tempo;
    private float[] energy;

    // Método para inicializar el agente
    public override void Initialize()
    {
        // Inicializar el entorno del agente aquí si es necesario
    }

    // Método para recolectar observaciones
    public override void CollectObservations(VectorSensor sensor)
    {
        // Recolectar observaciones del entorno
        sensor.AddObservation(tempo); // Añadir el tempo como observación
        foreach (float e in energy)
        {
            sensor.AddObservation(e); // Añadir la energía como observación
        }
    }

    // Método para realizar acciones
    public override void OnActionReceived(ActionBuffers actions)
    {
        // Realizar acciones en el entorno basadas en las salidas del modelo
        // Aquí debes implementar la lógica para aplicar las acciones al entorno de Unity
    }

    // Método para reiniciar el agente
    public override void OnEpisodeBegin()
    {
        // Reiniciar los datos de entrada y salidas
        tempo = Random.Range(60f, 180f); // Generar un tempo aleatorio entre 60 y 180 BPM
        energy = new float[10]; // Generar datos de energía aleatorios
        for (int i = 0; i < energy.Length; i++)
        {
            energy[i] = Random.Range(0f, 1f); // Generar valores de energía aleatorios entre 0 y 1
        }
    }
}