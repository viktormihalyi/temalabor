using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Nest;

namespace webscraper.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ProductController : ControllerBase
    {
        private readonly IElasticClient _elasticClient;
        public ProductController(IElasticClient elasticClient){
            _elasticClient = elasticClient;
        }
        // GET api/values
        [HttpGet]
        public async Task<IActionResult> Get()
        {
            
            return Ok("Teszt");
        }


        // GET api/products/name
        [HttpGet("search")]
        public async Task<IActionResult> Get(string category, string title)
        {   
            
            QueryContainer qContainer = new QueryContainer();
            QueryContainerDescriptor<Product> qcd = new QueryContainerDescriptor<Product>();

            if(category != null)
            {
                qContainer = qContainer && qcd.Match(m => m
                        .Field(f => f.Category)
                        .Query(category)
                );
            }
            if (title != null)
            {
                qContainer = qContainer && qcd.Match(m => m
                        .Field(f => f.Title)
                        .Query(title)
                );
            }
           
            var response = await _elasticClient.SearchAsync<Product>(s => s.Query(_ => qContainer));
            var products = response.Documents;

            return Ok(products);
        }

       
    }
}
