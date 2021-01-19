using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace AirSimUnity
{
    /// <summary>
    /// Changes opacity of the object "Target" depending on current control mode
    /// if car is driving by itself target is visible
    /// if car is being driven by a person target is 50% transparent
    /// </summary>
    public class targetTransparancy : MonoBehaviour
    {
        private GameObject carObject;
        private GameObject targetObject;
        private float transparentAlpha = 0.5f;
        private Color baseColor;
        private Car car;

        // Start is called before the first frame update
        void Start()
        {
            carObject = GameObject.Find("Car");
            car = carObject.GetComponent<Car>();
            targetObject = GameObject.Find("Target");
            baseColor = targetObject.GetComponent<Renderer>().material.color;
        }

        // Update is called once per frame
        void Update()
        {
            if (car.getApiEnabled())
            {
                makeVisible(targetObject.GetComponent<Renderer>().material, 1);
            }
            /*else
            {
                makeTransparent(targetObject.GetComponent<Renderer>().material, transparentAlpha);
            }*/
        }

        //https://github.com/Unity-Technologies/UnityCsReference/blob/master/Editor/Mono/Inspector/StandardShaderGUI.cs line 335

        void makeTransparent(Material mat, float alphaVal)
        {
            //preset for setting rendering mode of selected material to transparent
            mat.SetOverrideTag("RenderType", "Transparent");
            mat.SetInt("_SrcBlend", (int)UnityEngine.Rendering.BlendMode.One);
            mat.SetInt("_DstBlend", (int)UnityEngine.Rendering.BlendMode.OneMinusSrcAlpha);
            mat.SetInt("_ZWrite", 0);
            mat.DisableKeyword("_ALPHATEST_ON");
            mat.DisableKeyword("_ALPHABLEND_ON");
            mat.EnableKeyword("_ALPHAPREMULTIPLY_ON");
            mat.renderQueue = (int)UnityEngine.Rendering.RenderQueue.Transparent;
            //changing the alpha to increase opacity
            Color newColor = new Color(baseColor.r, baseColor.g, baseColor.b, alphaVal);
            mat.SetColor("_Color", newColor);
        }

        void makeVisible(Material mat, float alphaVal)
        {
            //preset for setting rendering mode of selected material to opaque(default for our target)
            mat.SetOverrideTag("RenderType", "");
            mat.SetInt("_SrcBlend", (int)UnityEngine.Rendering.BlendMode.One);
            mat.SetInt("_DstBlend", (int)UnityEngine.Rendering.BlendMode.Zero);
            mat.SetInt("_ZWrite", 1);
            mat.DisableKeyword("_ALPHATEST_ON");
            mat.DisableKeyword("_ALPHABLEND_ON");
            mat.DisableKeyword("_ALPHAPREMULTIPLY_ON");
            mat.renderQueue = -1;
            //changes alpha to 1 and makes target completely visible
            mat.SetColor("_Color", new Color(baseColor.r, baseColor.g, baseColor.b, 1));
        }
    }
}

