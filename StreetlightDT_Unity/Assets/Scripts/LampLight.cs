using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.IO;
using System.Net;
using System.Windows;
using System;
using System.Timers;
using Microsoft.MixedReality.Toolkit.UI;
using UnityEngine.Networking;

public class LampLight : MonoBehaviour
{
    private TextMeshPro textMesh;

    // Start is called before the first frame update
    void Start()
    {
        textMesh = GetComponent<TextMeshPro>();
    }

    public void OnSliderUpdated(SliderEventData eventData)
    {
        Color lampOff = new Color(0.9f, 0.9f, 0.9f, 0.3f);
        var sphereRenderer = GameObject.Find("Sphere").GetComponent<Renderer>();
        if (sphereRenderer.material.GetColor("_Color") != lampOff)
        {
            float brightness = (eventData.NewValue) * 100;
            textMesh.text = string.Format("Brightness: {0:N1}%", brightness);
        }
        else
        {
           textMesh.text = "Lamp is off";
        }
    }

    public void OnToggleSwitch()
    {
        Color lampOff = new Color(0.9f, 0.9f, 0.9f, 0.3f);
        var sphereRenderer = GameObject.Find("Sphere").GetComponent<Renderer>();
        if (sphereRenderer.material.GetColor("_Color") == lampOff)
        {
            textMesh.text = "Lamp is off";
        }
        else
        {
            textMesh.text = "Brightness: 100%";
        }
    }
}
