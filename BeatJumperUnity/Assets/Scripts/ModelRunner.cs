using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using Unity.Barracuda;

public class ModelRunner : MonoBehaviour
{
    public NNModel modelAsset;
    public Text speedText;
    public Text frequencyText;
    public Text heightText;

    private IWorker worker;
    private const int NUM_INPUTS = 11; // Adjust according to your input shape

    void Start()
    {
        var model = ModelLoader.Load(modelAsset);
        worker = WorkerFactory.CreateWorker(WorkerFactory.Type.ComputePrecompiled, model);

        // Example input values, replace with your own
        var tempo = Random.Range(60f, 180f);
        var energy = new float[NUM_INPUTS];
        for (int i = 0; i < energy.Length; i++)
        {
            energy[i] = Random.Range(0f, 1f);
        }

        // Normalize input values if needed
        // ...

        // Prepare input tensor
        Tensor inputTempo = new Tensor(1, 1, 1, 1);
        inputTempo[0] = tempo;
        Tensor inputEnergy = new Tensor(1, NUM_INPUTS, 1, 1, energy);

        // Execute model
        var inputs = new Dictionary<string, Tensor>();
        inputs["input_tempo"] = inputTempo;
        inputs["input_energy"] = inputEnergy;
        worker.Execute(inputs);

        // Get output tensors
        Tensor outputSpeed = worker.PeekOutput("output_speed");
        Tensor outputFrequency = worker.PeekOutput("output_frequency");
        Tensor outputHeight = worker.PeekOutput("output_height");

        // Process output values
        float speed = outputSpeed[0];
        float frequency = outputFrequency[0];
        float height = outputHeight[0];

        // Update UI or do something with the output values
        speedText.text = "Speed: " + speed.ToString();
        frequencyText.text = "Frequency: " + frequency.ToString();
        heightText.text = "Height: " + height.ToString();

        // Dispose tensors
        inputTempo.Dispose();
        inputEnergy.Dispose();
        outputSpeed.Dispose();
        outputFrequency.Dispose();
        outputHeight.Dispose();
    }

    void OnDestroy()
    {
        worker.Dispose();
    }
}
