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

    public GameObject Bunny;
    public GameObject PlatformManager;

    public static event Action OnModelReady; // Evento para notificar cuando el modelo está listo

    void Start()
    {
        DataReceiver.OnDataReceived += ProcessData;
    }

    // Método para procesar los datos recibidos
    public void ProcessData(float tempo, float[] energy, int energyLength)
    {
        try
        {
            Debug.Log("Inicializando modelo.");

            var model = ModelLoader.Load(modelAsset);
            worker = WorkerFactory.CreateWorker(WorkerFactory.Type.ComputePrecompiled, model);

            // Preparar los datos de entrada para el modelo
            var inputTempo = new Tensor(1, 1, 1, 1);
            inputTempo[0] = tempo;
            var inputEnergy = new Tensor(1, energyLength, 1, 1, energy);

            // Ejecutar el modelo con los datos de entrada
            var inputs = new Dictionary<string, Tensor>();
            inputs["inputs"] = inputTempo;
            inputs["inputs_1"] = inputEnergy;
            worker.Execute(inputs);

            // Obtener los tensores de salida
            var outputSpeed = worker.PeekOutput("output_0");
            var outputFrequency = worker.PeekOutput("output_1");
            var outputHeight = worker.PeekOutput("output_2");

            Debug.Log("Tensor de salida de velocidad: " + outputSpeed);
            Debug.Log("Tensor de salida de frecuencia: " + outputFrequency);
            Debug.Log("Tensor de salida de altura: " + outputHeight);

            // Procesar los valores de salida
            float speed = outputSpeed[0, 0, 0, 0];
            float frequency = outputFrequency[0, 0, 0, 0];
            // Obtener la longitud del tensor de altura
            int heightLength = outputHeight.length;

            // Crear un array para almacenar las alturas
            float[] heights = new float[heightLength];

            // Copiar los datos del tensor al array
            for (int i = 0; i < heightLength; i++)
            {
                heights[i] = outputHeight[0, i, 0, 0]; // El tensor es de forma (1, length, 1, 1)
            }
            
            Debug.Log("Velocidad: " + speed);
            Debug.Log("Frecuencia de generación de las plataformas: " + frequency);
            Debug.Log("Altura de las plataformas: " + string.Join(", ", heights));

            // Una vez que el modelo esté listo, activa el evento OnModelReady
            OnModelReady?.Invoke();

            BunnyMovement bunnyMovement = Bunny.GetComponent<BunnyMovement>();
            PlatformGenerator platformGenerator = PlatformManager.GetComponent<PlatformGenerator>();

            bunnyMovement.Speed = speed;
            platformGenerator.generationFrequency = frequency;
            platformGenerator.heights = heights;
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