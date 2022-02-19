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
using System.Globalization;
using Microsoft.MixedReality.Toolkit.UI;
using UnityEngine.Networking;
using SimpleJSON;

public class JsonLoader3 : MonoBehaviour
{
    public string jsonFile;
    public TextMeshPro textMesh;
    public float set_brightness;
    public string time;
    public string displayTime;
    public string displayLEDMode;
    //public Material wireFrameGlow;
    //public Material wireFrame;

    // Start is called before the first frame update
    void Start()
    {
        textMesh = GetComponent<TextMeshPro>();
        set_brightness = 100;
        StartCoroutine(UpdateValues());
    }

    public void OnSliderUpdated(SliderEventData eventData)
    {
        Color lampOff = new Color(0.9f, 0.9f, 0.9f, 0.3f);
        var sphereRenderer = GameObject.Find("Sphere").GetComponent<Renderer>();
        if (sphereRenderer.material.GetColor("_Color") != lampOff)
        {
            set_brightness = (eventData.NewValue) * 100;
        }
        else
        {
            set_brightness = 0;
        }
    }

    public void OnToggleSwitch()
    {
        Color lampOff = new Color(0.9f, 0.9f, 0.9f, 0.3f);
        var sphereRenderer = GameObject.Find("Sphere").GetComponent<Renderer>();
        if (sphereRenderer.material.GetColor("_Color") == lampOff)
        {
            set_brightness = 0;
        }
        else
        {
            set_brightness = 100;
        }
    }

    IEnumerator GetJson()
    {
        string uri = "http://192.168.1.246:5000/api?brightness=" + set_brightness.ToString();
        UnityWebRequest webRequest = UnityWebRequest.Get(uri);
        yield return webRequest.SendWebRequest();
        try
        {
            DateTime moment = DateTime.Now;
            int hour = moment.Hour;
            int minute = moment.Minute;
            if (minute >= 30)
            {
                time = hour.ToString() + ".5";
                displayTime = hour.ToString() + ":" + minute;
            }
            else if (minute < 10)
            {
                time = hour.ToString();
                displayTime = hour.ToString() + ":0" + minute;
            }
            else
            {
                time = hour.ToString();
                displayTime = hour.ToString() + ":" + minute;
            }
            JSONNode jsonFile = SimpleJSON.JSON.Parse(System.Text.Encoding.UTF8.GetString(webRequest.downloadHandler.data));
            string displayVoltage = jsonFile["real_data"]["voltage"].Value;
            string displayCurrent = jsonFile["real_data"]["current"].Value;
            string displayCarbonEmission = jsonFile["michael_data"][time]["carbon_emission"].Value;
            string displayElectricityToUse = jsonFile["michael_data"][time]["electricity_to_use"].Value;
            string displayElectricityGenerated = jsonFile["michael_data"][time]["electricity_generated"].Value;
            string displayBatterySoc = jsonFile["michael_data"][time]["battery_soc"].Value;
            string displayElectricityPrice = jsonFile["michael_data"][time]["electricity_price"].Value;
           
            string electricityToBuy = jsonFile["michael_data"][time]["electricity_to_buy"].Value;
            float electricityToBuyFloat = float.Parse(electricityToBuy) * 4f;
            string displayElectricityToBuy = electricityToBuyFloat.ToString();
            
            string LEDMode = jsonFile["michael_data"][time]["LED_mode"].Value;

            var pylonRenderer = GameObject.Find("pylon").GetComponent<MeshRenderer>();
            var batteryRenderer = GameObject.Find("battery").GetComponent<MeshRenderer>();
            Color greenGlow = new Color(0.0f, 0.25f, 0.0f, 0.8f);
            Color darkGrey = new Color(0.0f, 0.0f, 0.0f, 0.8f);
            if (LEDMode == "1")
            {
                displayLEDMode = "Battery";
                batteryRenderer.material.SetColor("_Color", greenGlow);
                pylonRenderer.material.SetColor("_Color", darkGrey);
            }
            else if (LEDMode == "2")
            {
                displayLEDMode = "Power grid";
                pylonRenderer.material.SetColor("_Color", greenGlow);
                batteryRenderer.material.SetColor("_Color", darkGrey);
            }
            else
            {
                displayLEDMode = "Unknown mode";
            }
            
            //string displayHourlyTraffic = jsonFile["michael_data"][time]["hourly_traffic"].Value;
            //string displayPV = jsonFile["michael_data"][time]["PV"].Value;
            string predictedTraffic = jsonFile["LSTM_data"][time]["predicted_traffic"].Value;

            DateTime thisDay = DateTime.Today;

            textMesh.text = $"LED voltage: {displayVoltage} V" +
                $"\nLED current: {displayCurrent} A" +
                $"\n\nDate: {thisDay.ToString("d")}" +
                $"\nTime: {displayTime}" +
                $"\nCarbon Emission: {displayCarbonEmission} gCO2/kWh" +
                $"\nElectricity to use: {displayElectricityToUse} Wh" +
                $"\nElectricity generated: {displayElectricityGenerated} Wh" +
                $"\nBattery SOC: {displayBatterySoc} Wh" +
                $"\nElectricity price: {displayElectricityPrice} €/MWh" +
                $"\nElectricity to buy: {displayElectricityToBuy} Ah" +
                $"\nLED mode: {displayLEDMode}" +
                //$"\nHourly traffic (cars and people): {displayHourlyTraffic}" +
                //$"\nPV: {displayPV} W/m^2" +
                $"\nPredicted traffic in next half hour (cars): {predictedTraffic}";
        }
        catch
        {
            Debug.Log("Network Error");
            textMesh.text = "Network Error";
        }
    }

    IEnumerator UpdateValues()
    {
        while (true)
        {
            StartCoroutine(GetJson());
            yield return new WaitForSeconds(0.1F);
        }
    }
}
