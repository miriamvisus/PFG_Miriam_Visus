using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Policies;

public class AudioAgent : Agent
{
    TensorFlowModel model;
    string modelUrl = "https://github.com/miriamvisus/PFG_Miriam_Visus_Martin/raw/main/BeatJumperPython/trained_model.h5";

    public override void Initialize()
    {
        // Descarga y carga el modelo de TensorFlow
        DownloadModel();
        model = new TensorFlowModel();
        model.Load(Application.persistentDataPath + "/trained_model.h5");
    }

    private void DownloadModel()
    {
        using (WebClient client = new WebClient())
        {
            client.DownloadFile(modelUrl, Application.persistentDataPath + "/trained_model.h5");
        }
    }

    private float tempo;
    private float[] energy;

    public override void CollectObservations(VectorSensor sensor)
    {
        // Recolecta observaciones del entorno y pasa las observaciones al modelo
        sensor.AddObservation(tempo); // Añade el tempo como observación
        foreach (float e in energy)
        {
            sensor.AddObservation(e); // Añade la energía como observación
        }
    }

    public override void OnActionReceived(ActionBuffers actions)
    {
        // Ejecuta inferencias basadas en las observaciones del entorno
        // Aquí puedes llamar al método de inferencia del modelo y obtener las acciones inferidas
        // Por ahora, simplemente imprimiremos las acciones recibidas
        Debug.Log("Action Received: " + actions.ContinuousActions);
    }

    public override void OnEpisodeBegin()
    {
        // Reinicia el entorno para comenzar un nuevo episodio
        tempo = Random.Range(60f, 180f); // Genera un tempo aleatorio entre 60 y 180 BPM
        energy = new float[10]; // Genera datos de energía aleatorios
        for (int i = 0; i < energy.Length; i++)
        {
            energy[i] = Random.Range(0f, 1f); // Genera valores de energía aleatorios entre 0 y 1
        }
    }
}
