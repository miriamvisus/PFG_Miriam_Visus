using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TensorFlow;
using System;
using System.IO;

public class TensorFlowModelLoader : MonoBehaviour
{
    // Ruta del modelo TensorFlow (.pb)
    public string modelPath = "C:/Users/miria.PORMIR/PFG_Miriam_Visus_Martin/BeatJumperPython/saved_model/saved_model.pb";

    // Referencia al modelo cargado
    private TFGraph graph;

    void Start()
    {
        // Cargar el modelo desde el archivo .pb
        graph = new TFGraph();

        // Cargar el contenido del archivo del modelo en un TFBuffer
        var modelBuffer = new TFBuffer(File.ReadAllBytes(modelPath));

        // Importar el modelo desde el TFBuffer
        graph.Import(modelBuffer);

        // Realizar una inferencia de prueba
        PerformInference();
    }

    void PerformInference()
    {
        // Crear el objeto de sesión para ejecutar el grafo
        using (var session = new TFSession(graph))
        {
            // Obtener la entrada y salida del grafo
            var inputOp = graph["input_node"][0];
            var outputOp = graph["output_node"][0];

            // Preparar los datos de entrada
            float[,] inputData = new float[1, 2] { { 1.0f, 2.0f } };

            // Calcular el tamaño total del array unidimensional
            int totalSize = inputData.GetLength(0) * inputData.GetLength(1);

            // Crear el array unidimensional
            float[] flattenedInputData = new float[totalSize];

            // Convertir la matriz bidimensional al array unidimensional
            int index = 0;
            for (int i = 0; i < inputData.GetLength(0); i++)
            {
                for (int j = 0; j < inputData.GetLength(1); j++)
                {
                    flattenedInputData[index++] = inputData[i, j];
                }
            }

            // Crear el tensor con los datos de entrada
            var inputTensor = new TFTensor(flattenedInputData);

            // Ejecutar el grafo para realizar una inferencia
            var output = session.Run(new[] { inputOp }, new TFTensor[] { inputTensor }, new[] { outputOp });

            // Obtener los resultados de la inferencia
            var result = (float[,])output[0].GetValue();
            Debug.Log("Resultado de la inferencia: " + result[0, 0]);
        }
    }

    void OnDestroy()
    {
        // Liberar los recursos al destruir el objeto
        if (graph != null)
        {
            graph.Dispose();
        }
    }
}