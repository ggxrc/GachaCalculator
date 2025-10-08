package com.ads.dorisolucoes

import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.AutoCompleteTextView
import androidx.core.widget.addTextChangedListener
import android.widget.EditText
import android.widget.RadioGroup
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class ExploracaoActivity : AppCompatActivity() {

    private val preco_nacoes = mapOf<String, Double>(
        "Mondstadt" to  35.0,
        "Liyue" to  40.0,
        "Inazuma" to  50.0,
        "Sumeru" to  100.0,
        "Fontaine" to  55.0,
        "Natlan" to  60.0,
    )

    private val precos_bussola = mapOf(

        "sem desconto" to 0.0,
        "Mondstadt" to  (1 - 0.05), // 5% de desconto
        "Liyue" to (1 - 0.11), // 11% de desconto
        "Inazuma" to  (1 - 0.17), // 17% de desconto
        "Sumeru" to  (1 - 0.25), // 25% de desconto
        "Fontaine" to  (1 - 0.12), // 12% de desconto
        "Natlan" to  (1 - 0.15), // 15% de desconto
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_exploracao)
        val nacoes = findViewById<AutoCompleteTextView>(R.id.nacoes)
        val total_explorado = findViewById<EditText>(R.id.total_explorado)
        val bussola = findViewById<RadioGroup>(R.id.rgBussola)

        calcularResultado(nacoes)

        nacoes.addTextChangedListener {
            calcularResultado(nacoes)
        }
        total_explorado.addTextChangedListener {
            calcularResultado(nacoes)
        }
        bussola.setOnCheckedChangeListener { _, _ ->
            calcularResultado(nacoes)
        }
    }
    fun escolherNacao(nacoes: AutoCompleteTextView, onNacaoEscolhida: (String?, Double?) -> Unit) {
        val nacoes_array = resources.getStringArray(R.array.nacoes_array)
        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, nacoes_array)
        nacoes.setAdapter(adapter)

        val nome = nacoes.text.toString()
        val preco = preco_nacoes[nome]
        onNacaoEscolhida(nome, preco)
    }

    fun aplicarDescontos(nacoes: AutoCompleteTextView, preco: Double?): Double {
        if (preco == null) return 0.0
        val total_explorado = findViewById<EditText>(R.id.total_explorado)
        val bussola = findViewById<RadioGroup>(R.id.rgBussola)

        var porcentagemExploracao = total_explorado.text.toString().toDoubleOrNull() ?: 0.0
        var descontoExploracao = (0.45 * porcentagemExploracao) / 100

        total_explorado.addTextChangedListener{

            porcentagemExploracao = total_explorado.text.toString().toDoubleOrNull() ?: 0.0
            descontoExploracao = (0.45 * porcentagemExploracao) / 100
        }
        if ((descontoExploracao * 100) > 36)
            descontoExploracao = 0.36

        val descontoBussola = if (bussola.checkedRadioButtonId == R.id.rbBussolaSim) {
            precos_bussola[nacoes.text.toString()]
        } else precos_bussola["sem desconto"]

        return if(descontoBussola != 0.0) preco *  ( (1 - descontoExploracao) * descontoBussola!!)
        else preco * (1 - descontoExploracao)
    }

    private fun calcularResultado(nacoes: AutoCompleteTextView) {
        val valor_total = findViewById<TextView>(R.id.resultado)

        escolherNacao(nacoes) { nome: String?, preco: Double? ->

            if (nome != null && preco != null) {
                val preco_descontado = aplicarDescontos(nacoes, preco)
                valor_total.text = "A região de $nome custará R$$preco_descontado"
            } else {
                valor_total.text = "preencha os campos acima"
            }
        }
    }
}