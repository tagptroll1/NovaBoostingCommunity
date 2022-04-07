using Microsoft.EntityFrameworkCore;

namespace MythicPlus
{
    public class MythicPlusDbContext : DbContext
    {
        public MythicPlusDbContext(DbContextOptions<MythicPlusDbContext> options) : base(options)
        {  }

    }
}