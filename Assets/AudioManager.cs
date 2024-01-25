using UnityEngine;

public class AudioManager : MonoBehaviour
{
    public AudioSource musicSource;

    public void PlayMusic(string musicPath)
    {
        AudioClip musicClip = Resources.Load<AudioClip>(musicPath);
        
        if (musicClip != null)
        {
            musicSource.clip = musicClip;
            musicSource.Play();
        }
        else
        {
            Debug.LogError("No se pudo cargar la música.");
        }
    }
}
