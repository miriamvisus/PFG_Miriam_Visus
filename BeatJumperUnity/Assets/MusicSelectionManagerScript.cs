using UnityEngine;
using UnityEngine.UI;

public class MusicSelectionManager : MonoBehaviour
{
    public AudioSource musicPlayer; // Asegúrate de asignar esto en el Inspector de Unity
    public Button[] songButtons; // Asigna los botones en el Inspector de Unity

    void Start()
    {
        // Asigna la función OnButtonClick al evento onClick de cada botón
        foreach (Button button in songButtons)
        {
            button.onClick.AddListener(() => OnButtonClick(button));
        }
    }

    // Función llamada cuando se hace clic en un botón
    void OnButtonClick(Button button)
    {
        // Obtén el nombre de la canción desde el texto del botón
        string songName = button.GetComponentInChildren<Text>().text;

        // Llama a la función para cargar y reproducir la canción
        LoadAndPlaySong(songName);
    }

    // Función para cargar y reproducir la canción
    void LoadAndPlaySong(string songName)
    {
        // Aquí deberías cargar y reproducir la canción utilizando tu lógica específica
        // Puedes usar AudioManager o cualquier otro método que hayas implementado para reproducir música
    }
}
