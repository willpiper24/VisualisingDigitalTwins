using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Microsoft.MixedReality.Toolkit.UI;

public class ToggleSlider : MonoBehaviour
{
    [SerializeField]
    private Renderer TargetRenderer;

    public void OnSliderUpdated(SliderEventData eventData)
    {
        Color lampGlow = new Color(1.0f, 1.0f, 0.5f, eventData.NewValue);
        Color lampOff = new Color(0.9f, 0.9f, 0.9f, 0.3f);
        TargetRenderer = GetComponentInChildren<Renderer>();
        if ((TargetRenderer != null) && (TargetRenderer.material != null) && (TargetRenderer.material.GetColor("_Color") != lampOff))
        {
            TargetRenderer.material.SetColor("_Color", lampGlow);
        }
    }
}
