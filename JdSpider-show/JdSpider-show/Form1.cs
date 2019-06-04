using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using MySql.Data.MySqlClient;
using System.Windows.Forms.DataVisualization.Charting;

namespace JdSpider_show
{
    public partial class Form1 : Form
    {
        MySqlConnection con = new MySqlConnection(@"server=localhost;database=jdspider;user id=root;pwd=root");

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            con.Open();
        }

        private void do_show_in_table(string sql)
        {
            MySqlDataAdapter data = new MySqlDataAdapter(sql, con);
            DataSet ds = new DataSet();            
            data.Fill(ds);
            con.Close();
            dataGridView1.AutoGenerateColumns = false;
            dataGridView1.DataSource = ds.Tables[0];
        }


        private void button1_Click(object sender, EventArgs e)
        {
            string sql = "SELECT * FROM data";
            do_show_in_table(sql);
        }
        private void button2_Click(object sender, EventArgs e)
        {
            string sql = "SELECT * FROM data WHERE " + comboBox1.Text + "='" + textBox1.Text + "'";
            do_show_in_table(sql);
        }

        private void button3_Click(object sender, EventArgs e)
        {
            string sql = "SELECT * FROM data WHERE price" + textBox2.Text;
            do_show_in_table(sql);
        }

        private void button4_Click(object sender, EventArgs e)
        {
            string colname = comboBox2.Text;
            string sql = "SELECT * FROM data WHERE " + colname + "<>''";

            DataSet ds = new DataSet();
            try
            {
                MySqlDataAdapter data = new MySqlDataAdapter(sql, con);
                
                data.Fill(ds);
                con.Close();
                dataGridView1.DataSource = ds.Tables[0];
            }
            catch { return; }

            Dictionary<string, int> result = new Dictionary<string, int>();
            foreach (DataRow row in ds.Tables[0].Rows)
            {
                string colvalue = row[colname].ToString();
                if (result.ContainsKey(colvalue))
                {
                    result[colvalue]++;
                }
                else
                {
                    result.Add(colvalue, 1);
                }
            }
            
            List<KeyValuePair<string, int>> lst = new List<KeyValuePair<string, int>>(result);
            lst.Sort(delegate (KeyValuePair<string, int> s1, KeyValuePair<string, int> s2) {
                return s2.Value.CompareTo(s1.Value);
            });

            chart1.Series[0]["PieLabelStyle"] = "Outside";//将文字移到外侧
            chart1.Series[0]["PieLineColor"] = "Black";//绘制黑色的连线。
            chart1.Series[0].XValueType = ChartValueType.String;

            Dictionary<string, int> show_result = new Dictionary<string, int>();
            for (int i = 0;i < lst.Count; i++)
            {
                if (i <= 10)
                {
                    show_result.Add(lst[i].Key, lst[i].Value);
                }
                else
                {
                    if (show_result.ContainsKey("其他"))
                        show_result["其他"]++;
                    else
                        show_result.Add("其他", 0);
                }
            }

            chart1.Series[0].Points.DataBindXY(show_result.Keys.ToList<string>(), show_result.Values.ToList<int>());
        }
    }
}
