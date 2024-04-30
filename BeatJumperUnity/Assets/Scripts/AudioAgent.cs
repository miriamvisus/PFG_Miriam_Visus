using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using Unity.MLAgents.Actuators;
using TensorFlow;
using System.IO;

public class AudioAgent : Agent
{
    TFGraph graph;
    TFSession session;
    
    // Ruta del modelo TensorFlow (.pb)
    [SerializeField] private string modelPath = "C:/Users/miria.PORMIR/PFG_Miriam_Visus_Martin/BeatJumperPython/saved_model/saved_model.pb";

    float tempo;
    float[] energy;

    public override void Initialize()
    {
        // Cargar el contenido del archivo del modelo en un TFBuffer
        var modelBuffer = new TFBuffer(File.ReadAllBytes(modelPath));

        // Importar el modelo desde el TFBuffer
        graph = new TFGraph();
        graph.Import(modelBuffer);

        // Inicializar la sesión TensorFlow
        session = new TFSession(graph);
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        // Recolectar observaciones del entorno y pasarlas al modelo
        sensor.AddObservation(tempo); // Agregar el tempo como observación
        foreach (float e in energy)
        {
            sensor.AddObservation(e); // Agregar la energía como observación
        }
    }

    public override void OnActionReceived(ActionBuffers actions)
    {
        // Ejecutar inferencias basadas en las observaciones del entorno
        // Llamar al método de inferencia del modelo y obtener las acciones inferidas
        TFTensor[] inputs = new TFTensor[]
        {
            new TFTensor(new float[] { tempo }),
            new TFTensor(energy)
        };

        TFSession.Runner runner = session.GetRunner();
        runner.AddInput(graph["input_tempo"][0], inputs[0]);
        runner.AddInput(graph["input_energy"][0], inputs[1]);
        runner.Fetch(graph["output_speed"][0]);
        runner.Fetch(graph["output_frequency"][0]);
        runner.Fetch(graph["output_height"][0]);

        TFTensor[] outputs = runner.Run();

        // Procesar las salidas del modelo
        float speed = (float)outputs[0].GetValue();
        float frequency = (float)outputs[1].GetValue();
        float height = (float)outputs[2].GetValue();

        Debug.Log("Action Received - Speed: " + speed + ", Frequency: " + frequency + ", Height: " + height);
    }

    public override void OnEpisodeBegin()
    {
        // Reiniciar el entorno para comenzar un nuevo episodio
        tempo = Random.Range(60f, 180f); // Generar un tempo aleatorio entre 60 y 180 BPM
        energy = new float[10]; // Generar datos de energía aleatorios
        for (int i = 0; i < energy.Length; i++)
        {
            energy[i] = Random.Range(0f, 1f); // Generar valores de energía aleatorios entre 0 y 1
        }
    }
}
