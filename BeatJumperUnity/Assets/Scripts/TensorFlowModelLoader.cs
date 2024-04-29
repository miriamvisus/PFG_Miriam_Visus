using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TensorFlowLite;
using System;

public class TensorFlowModelLoader : MonoBehaviour
{
    // Ruta del modelo TensorFlow (.pb)
    public string modelPath = "C:/Users/miria.PORMIR/PFG_Miriam_Visus_Martin/BeatJumperPython/saved_model/saved_model.pb";

    // Nombres de entrada y salida del modelo
    public string inputNames;
    public string outputNames;

    private Interpreter interpreter;

    void Start()
    {
        // Dividir los nombres de entrada utilizando una coma como delimitador
        string[] inputNameArray = inputNames.Split(',');

        // Dividir los nombres de salida utilizando una coma como delimitador
        string[] outputNameArray = outputNames.Split(',');

        // Cargar el modelo TensorFlow
        interpreter = new Interpreter(modelPath);

        // Opcional: Configurar las opciones del modelo si es necesario
        interpreter.UseNNAPI = false; // Deshabilitar NNAPI si no es compatible con el dispositivo

        // Opcional: Inicializar el intérprete
        foreach (string inputName in inputNameArray)
        {
            // Supongamos que todos los inputs son de tamaño 1
            interpreter.ResizeInput(inputName.Trim(), new int[] { 1 });
        }
        interpreter.AllocateTensors();

        // Ejemplo de cómo usar el modelo
        // Estos son solo valores de ejemplo, debes ajustarlos según tu aplicación
        float tempo = 120.0f; // Ejemplo de valor de entrada para el tempo
        float[] energy = new float[] { 0.5f, 0.3f, 0.2f }; // Ejemplo de valor de entrada para la energía

        // Ejecutar la inferencia
        interpreter.SetInputTensorData(inputNameArray[0].Trim(), new float[] { tempo });
        interpreter.SetInputTensorData(inputNameArray[1].Trim(), energy);
        interpreter.Invoke();

        // Obtener los resultados de la inferencia
        float[] outputSpeed = interpreter.GetOutputTensorData(outputNameArray[0].Trim());
        float[] outputFrequency = interpreter.GetOutputTensorData(outputNameArray[1].Trim());
        float[] outputHeight = interpreter.GetOutputTensorData(outputNameArray[2].Trim());

        // Procesamiento de los resultados si es necesario

        // Ejemplo: Imprimir los resultados
        Debug.Log("Output Speed: " + outputSpeed[0]);
        Debug.Log("Output Frequency: " + outputFrequency[0]);
        Debug.Log("Output Height: " + outputHeight[0]);
    }

    private void OnDestroy()
    {
        // Liberar los recursos
        if (interpreter != null)
        {
            interpreter.Dispose();
        }
    }
}