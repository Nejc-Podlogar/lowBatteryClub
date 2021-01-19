using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO.Ports;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using UnityEngine.UI;
using System.Threading;

namespace AirSimUnity
{

    public class STM32F411_data : MonoBehaviour
    {
        // Start is called before the first frame update
        private GameObject carObject;
        private Car car;
        SerialPort _serialPort;
        string message;
        bool run = true;
        float prevY, curY;

        public GameObject TextMag;
        public GameObject TextAcc;
        public GameObject TextGyro;
        public GameObject STM32Blend;

        private TcpClient client;
        private NetworkStream networkStream;
        private Byte[] data;

        private Thread _t1;

        private List<string> readData = new List<string>();
        string responseData;
        void Start()
        {
            //SerialPort init
            //try
            //{
            //_serialPort = new SerialPort();
            //_serialPort.PortName = "COM8";
            //_serialPort.BaudRate = 115200;
            //_serialPort.DataBits = 8;
            //_serialPort.Parity = Parity.None;
            //_serialPort.StopBits = StopBits.One;
            //_serialPort.Handshake = Handshake.None;

            //}
            //catch (Exception e)
            //{
            //    run = false;
            //}

            //tcpClient = new TcpClient("127.0.0.1", 65432)
            //NewtorkStream stream = tcpClient.GetStream();

            //client = new TcpClient("127.0.0.1", 65432);
            //networkStream = client.GetStream();
            //data = new byte[256];
            //message = "";
            //responseData = string.Empty;

            //Car object init
            carObject = GameObject.Find("Car");
            car = carObject.GetComponent<Car>();

            TextMag = GameObject.Find("TextMagVals");
            TextAcc = GameObject.Find("TextAccVals");
            TextGyro = GameObject.Find("TextGyroVals");
            STM32Blend = GameObject.Find("STM32blend");

            STM32Blend.transform.Rotate(0, -90, 0, Space.Self);

            client = new TcpClient("127.0.0.1", 65432);
            networkStream = client.GetStream();
            data = new byte[256];
            message = "";
            responseData = string.Empty;

            _t1 = new Thread(threadFunction);
            _t1.Start();
            //try
            //{
            //    _serialPort.Open();
            //}
            //catch (Exception ex)
            //{
            //    Debug.Log(ex.Message);
            //    run = false;
            //}
        }

        private void threadFunction()
        {
            try
            {
                for (; ; )
                {

                    //message = _serialPort.ReadLine();
                    Int32 bytes = networkStream.Read(data, 0, data.Length);
                    responseData = Encoding.ASCII.GetString(data, 0, bytes);
                    //textBox1.AppendText(responseData + Environment.NewLine);

                    readData = responseData.Split(',').ToList();

                    //Debug.Log(responseData);


                    //List<float> readData = message.Split(',').Select(float.Parse).ToList();

                    //if (readData.Count() == 9)
                    //{
                    //    TextMag.GetComponent<Text>().text = (readData[0] + " " + readData[1] + " " + readData[2]);
                    //    TextAcc.GetComponent<Text>().text = (readData[3] + " " + readData[4] + " " + readData[5]);
                    //    TextGyro.GetComponent<Text>().text = (readData[6] + " " + readData[7] + " " + readData[8]);
                    //}
                    //else
                    //{
                    //    TextMag.GetComponent<Text>().text = "0.000 0.000 0.000";
                    //    TextAcc.GetComponent<Text>().text = "0.000 0.000 0.000";
                    //    TextGyro.GetComponent<Text>().text = "0.000 0.000 0.000";
                    //}
                }
            }
            catch (Exception e)
            {
                readData = new List<string>();
            }
        }
        // Update is called once per frame
        void Update()
        {
            curY = car.transform.eulerAngles.y;
            this.transform.position = carObject.transform.position + carObject.transform.right * 4;
            this.transform.position += new Vector3(0, 2, 0);

            this.transform.Rotate(0, curY - prevY, 0, Space.Self);


            STM32Blend.transform.position = carObject.transform.position + carObject.transform.right * 2;
            STM32Blend.transform.position += new Vector3(0, 1, 0);
            STM32Blend.transform.Rotate(0, curY - prevY, 0, Space.Self);

            prevY = curY;


            if (readData.Count() == 9)
            {
                TextMag.GetComponent<Text>().text = (readData[0] + " " + readData[1] + " " + readData[2]);
                TextAcc.GetComponent<Text>().text = (readData[3] + " " + readData[4] + " " + readData[5]);
                TextGyro.GetComponent<Text>().text = (readData[6] + " " + readData[7] + " " + readData[8]);

                //Debug.Log(Convert.ToDouble(readData[6].Replace(".",",")));

                if (Convert.ToDouble(readData[6].Replace(".", ",")) > 5.0)
                {
                    STM32Blend.transform.Rotate(1, 0, 0);
                }
                if (Convert.ToDouble(readData[6].Replace(".", ",")) < -5.0)
                {
                    STM32Blend.transform.Rotate(-1, 0, 0);
                }

                if (Convert.ToDouble(readData[7].Replace(".", ",")) > 5.0)
                {
                    STM32Blend.transform.Rotate(0, 0, 1);
                }
                if (Convert.ToDouble(readData[7].Replace(".", ",")) < -5.0)
                {
                    STM32Blend.transform.Rotate(0, 0, -1);
                }

                if (Convert.ToDouble(readData[8].Replace(".", ",")) > 5.0)
                {
                    STM32Blend.transform.Rotate(0, -1, 0);
                }
                if (Convert.ToDouble(readData[8].Replace(".", ",")) < -5.0)
                {
                    STM32Blend.transform.Rotate(0, 1, 0);
                }
                //if (readData[7] > 2.0 || readData[7] > 2.0)
                //{

                //}
                //if (readData[8] > 2.0 || readData[8] > 2.0)
                //{

                //}
            }
            else
            {
                TextMag.GetComponent<Text>().text = "0.000 0.000 0.000";
                TextAcc.GetComponent<Text>().text = "0.000 0.000 0.000";
                TextGyro.GetComponent<Text>().text = "0.000 0.000 0.000";
            }

            //if (run)
            //{
            //    try
            //    {
            //        //message = _serialPort.ReadLine();
            //        Int32 bytes = networkStream.Read(data, 0, data.Length);
            //        responseData = Encoding.ASCII.GetString(data, 0, bytes);
            //        //textBox1.AppendText(responseData + Environment.NewLine);

            //        List<string> readData = responseData.Split(',').ToList();

            //        //Debug.Log(responseData);


            //        //List<float> readData = message.Split(',').Select(float.Parse).ToList();

            //        if (readData.Count() == 9)
            //        {
            //            TextMag.GetComponent<Text>().text = (readData[0] + " " + readData[1] + " " + readData[2]);
            //            TextAcc.GetComponent<Text>().text = (readData[3] + " " + readData[4] + " " + readData[5]);
            //            TextGyro.GetComponent<Text>().text = (readData[6] + " " + readData[7] + " " + readData[8]);
            //        }
            //        else
            //        {
            //            TextMag.GetComponent<Text>().text = "0.000 0.000 0.000";
            //            TextAcc.GetComponent<Text>().text = "0.000 0.000 0.000";
            //            TextGyro.GetComponent<Text>().text = "0.000 0.000 0.000";
            //        }

            //    }
            //    catch (TimeoutException e)
            //    {

            //    }
            //}
        }
    }
}