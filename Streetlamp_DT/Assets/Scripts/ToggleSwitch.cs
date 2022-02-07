using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ToggleSwitch : MonoBehaviour
{
    public void VirtualLight()
    {
        Color lampGlow = new Color(1.0f, 1.0f, 0.5f);
        Color lampOff = new Color(0.9f, 0.9f, 0.9f, 0.3f);
        var sphereRenderer = GetComponent<Renderer>();
        if (sphereRenderer.material.GetColor("_Color") == lampOff)
        {
            sphereRenderer.material.SetColor("_Color", lampGlow);
            //sphereRenderer.material.SetColor("_EmissionColor", Color.black);
            //sphereRenderer.material.EnableKeyword("_EMISSION");
        }
        else
        {
            sphereRenderer.material.SetColor("_Color", lampOff);
            //sphereRenderer.material.SetColor("_EmissionColor", Color.black);
            //sphereRenderer.material.EnableKeyword("_EMISSION");
        }
    }
}
