using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TensorFlow;
using System;

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
        graph.Import(modelPath);

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

            // Preparar los datos de entrada (ejemplo)
            var inputTensor = new TFTensor(new float[1, 2] { { 1.0f, 2.0f } });

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