package com.ads.dorisolucoes

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class MainActivity : AppCompatActivity() {

    private lateinit var continuar_btn : Button // Botão 👍
    private var item_selecionado : View? = null // apenas para marcar e desmarcar o item selecionado
    private var servico_selecionado : Servico? = null // usado pra ir pro serviço em questão


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        carregarServicos()
        continuar_btn.setOnClickListener {
            startActivity(Intent(this, servico_selecionado?.destino))
        }
    }
    private fun carregarServicos(){
        val containerServicos = findViewById<LinearLayout>(R.id.containerServicos)
        val servicos = ServicosRepository.getServicos()

        servicos.forEach { servico ->
            val itemView = criarItemServico(servico, containerServicos)
            containerServicos.addView(itemView)
        }
    }
    private fun criarItemServico(servico: Servico, parent: ViewGroup): View {

        val itemView = layoutInflater.inflate(R.layout.item_servico, parent, false)

        val ivImagem = itemView.findViewById<ImageView>(R.id.ivServicoImagem)
        val tvNome = itemView.findViewById<TextView>(R.id.tvServicoNome)
        val tvDescricao = itemView.findViewById<TextView>(R.id.tvServicoDescricao)

        continuar_btn = findViewById(R.id.continuar)

        ivImagem.setImageResource(servico.imagemId)
        tvNome.text = servico.nome
        tvDescricao.text = servico.desc

        itemView.setOnClickListener {

            item_selecionado?.setBackgroundResource(R.drawable.bg_servico) // Remove a seleção do item anterior
            itemView.setBackgroundResource(R.drawable.bg_servico_selecionado) // Adiciona a seleção ao novo item
            item_selecionado = itemView // Atualiza o item selecionado
            Toast.makeText(this, "Selecionou: ${servico.nome}", Toast.LENGTH_SHORT).show()

            servico_selecionado = servico
            continuar_btn.isEnabled = true
        }
        return itemView
    }
}