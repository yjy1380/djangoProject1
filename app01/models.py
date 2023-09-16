from django.db import models


class Disease(models.Model):
    title = models.CharField(verbose_name='标题', max_length=32)

    def __str__(self):
        return self.title


class miRNA(models.Model):
    miRNAname = models.CharField(verbose_name="miRNA name", max_length=24)
    EvidenceCode = models.CharField(verbose_name="Evidence Code", max_length=24)
    Diseasename = models.CharField(verbose_name="Disease name", max_length=36)
    PMID = models.IntegerField(verbose_name="PMID")
    Description = models.CharField(verbose_name="Description", max_length=1024)
    Causality = models.CharField(verbose_name="Causality", max_length=1024)

    def __str__(self):
        return self.title
    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门ID")
    # 1.有约束
    #   - to，与那张表关联
    #   - to_field，表中的那一列关联
    # 2.django自动
    #   - 写的depart
    #   - 生成数据列 depart_id
    # 3.部门表被删除
    # ### 3.1 级联删除
    # depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
    # ### 3.2 置空
    # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    # 在django中做的约束
    # gender_choices = (
    #     (1, "男"),
    #     (2, "女"),
    # )
    # gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
