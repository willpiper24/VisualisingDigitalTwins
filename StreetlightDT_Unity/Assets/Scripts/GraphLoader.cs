using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;

public class GraphLoader : MonoBehaviour
{
    public Image image;
    RawImage m_RawImage;

    // Start is called before the first frame update
    void Start()
    {
        m_RawImage = GetComponent<RawImage>();
        StartCoroutine(UpdateValues());
    }

    IEnumerator DownloadImage(string MediaUrl)
    {
        UnityWebRequest request = UnityWebRequestTexture.GetTexture(MediaUrl);
        yield return request.SendWebRequest();
        try
        {
            m_RawImage.texture = ((DownloadHandlerTexture)request.downloadHandler).texture;
        }
        catch
        {
            Debug.Log("Network error");
        }
    }

    IEnumerator UpdateValues()
    {
        while (true)
        {
            // INSERT RAPSBERRY PI IP ADDRESS BELOW
            StartCoroutine(DownloadImage("http://IP_ADDRESS_HERE:5000/get_image"));
            yield return new WaitForSeconds(5);
        }
    }
}
