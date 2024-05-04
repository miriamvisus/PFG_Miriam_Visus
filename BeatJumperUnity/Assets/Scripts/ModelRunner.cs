using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using Unity.Barracuda;


public class ModelRunner : MonoBehaviour
{
    // Variables para las referencias a los objetos de la UI y el modelo
    public NNModel modelAsset;

    private IWorker worker;
    private const int NUM_INPUTS = 2; 

    public GameObject Bunny;
    public GameObject PlatformManager;

    public static event Action OnModelReady; // Evento para notificar cuando el modelo está listo

    void Start()
    {
        DataReceiver.OnDataReceived += ProcessData;
    }

    // Método para procesar los datos recibidos
    public void ProcessData(float tempo, float[] energy)
    {
        try
        {
            Debug.Log("Inicializando modelo.");

            var model = ModelLoader.Load(modelAsset);
            worker = WorkerFactory.CreateWorker(WorkerFactory.Type.ComputePrecompiled, model);

            // Preparar los datos de entrada para el modelo
            var inputTempo = new Tensor(1, 1, 1, 1);
            inputTempo[0] = tempo;
            var inputEnergy = new Tensor(1, NUM_INPUTS, 1, 1, energy);

            // Ejecutar el modelo con los datos de entrada
            var inputs = new Dictionary<string, Tensor>();
            inputs["input_tempo"] = inputTempo;
            inputs["input_energy"] = inputEnergy;
            worker.Execute(inputs);

            // Obtener los tensores de salida
            var outputSpeed = worker.PeekOutput("output_speed");
            var outputFrequency = worker.PeekOutput("output_frequency");
            var outputHeight = worker.PeekOutput("output_height");

            // Procesar los valores de salida
            float speed = outputSpeed[0];
            float frequency = outputFrequency[0];
            // Obtener la longitud del tensor de altura
            int heightLength = outputHeight.length;

            // Crear un array para almacenar las alturas
            float[] heights = new float[heightLength];

            // Copiar los datos del tensor al array
            for (int i = 0; i < heightLength; i++)
            {
                heights[i] = outputHeight[0, i, 0, 0]; // El tensor es de forma (1, length, 1, 1)
            }

            // Una vez que el modelo esté listo, activa el evento OnModelReady
            OnModelReady?.Invoke();

            // Obtener los scripts BunnyMovement y PlatformGenerator
            BunnyMovement bunnyScript = Bunny.GetComponent<BunnyMovement>();
            PlatformGenerator platformScript = PlatformManager.GetComponent<PlatformGenerator>();

            // Actualizar las variables en los scripts BunnyMovement y PlatformGenerator
            bunnyScript.Speed = speed;
            platformScript.generationFrequency = frequency;
            platformScript.heights = heights;
        }

        catch (System.Exception e)
        {
            Debug.LogError("Error al procesar datos: " + e.Message);
        }

        finally
        {
            // Liberar los tensores
            if (worker != null)
            {
                worker.Dispose();
            }
        }
    }

    void OnDestroy()
    {
        DataReceiver.OnDataReceived -= ProcessData;
    }
}